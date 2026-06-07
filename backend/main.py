from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from database import SessionLocal, engine, Base
import models
import schemas
import services

# Force create all tables with explicit echo
print("[INFO] Initializing database...")
Base.metadata.create_all(bind=engine)
print("[SUCCESS] Database tables created!")

app = FastAPI(title="Question Filter API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Question Filter API is running"}

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """Upload PDF files for processing"""
    try:
        uploaded_files = []
        
        for file in files:
            # Create upload directory if it doesn't exist
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(upload_dir, filename)
            
            # Save the file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Create file record in database
            db_file = models.UploadedFile(
                filename=filename,
                original_name=file.filename,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                status="uploaded"
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            uploaded_files.append({
                "id": db_file.id,
                "filename": db_file.filename,
                "original_name": db_file.original_name,
                "status": db_file.status
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Successfully uploaded {len(uploaded_files)} files",
                "files": uploaded_files
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/{file_id}")
async def process_file(file_id: int, db: Session = Depends(get_db)):
    """Process a single uploaded file"""
    try:
        # Get file from database
        db_file = db.query(models.UploadedFile).filter(models.UploadedFile.id == file_id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Update status
        db_file.status = "processing"
        db.commit()
        
        # Extract text from PDF
        text = services.extract_text_from_pdf(db_file.file_path)
        
        # Extract questions from text
        questions = services.extract_questions(text)
        
        # Save questions to database
        for question_text in questions:
            # Check if question already exists
            existing_question = db.query(models.Question).filter(
                models.Question.text == question_text
            ).first()
            
            if existing_question:
                # Increment repeat count
                existing_question.repeat_count += 1
                # Add this file as a source
                existing_question.sources.append(db_file.original_name)
            else:
                # Create new question
                new_question = models.Question(
                    text=question_text,
                    unit=services.detect_unit(question_text),
                    source=db_file.original_name,
                    repeat_count=1
                )
                db.add(new_question)
        
        # Update file status
        db_file.status = "processed"
        db.commit()
        
        return {"message": "File processed successfully", "file_id": file_id}
    except Exception as e:
        # Update status to error
        db_file.status = "error"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/questions/")
def get_questions(
    unit: Optional[str] = None,
    source: Optional[str] = None,
    min_repeats: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get questions with optional filters"""
    query = db.query(models.Question)
    
    if unit:
        query = query.filter(models.Question.unit == unit)
    
    if source:
        query = query.filter(models.Question.source.contains(source))
    
    if min_repeats:
        query = query.filter(models.Question.repeat_count >= min_repeats)
    
    questions = query.order_by(models.Question.repeat_count.desc()).all()
    
    return [
        {
            "id": q.id,
            "text": q.text,
            "unit": q.unit,
            "source": q.source,
            "repeat_count": q.repeat_count,
            "created_at": q.created_at
        }
        for q in questions
    ]

@app.get("/units/")
def get_units(db: Session = Depends(get_db)):
    """Get all unique units"""
    units = db.query(models.Question.unit).distinct().all()
    return [unit[0] for unit in units if unit[0]]

@app.get("/sources/")
def get_sources(db: Session = Depends(get_db)):
    """Get all unique sources"""
    sources = db.query(models.Question.source).distinct().all()
    return [source[0] for source in sources if source[0]]

@app.get("/export/csv/")
def export_csv(db: Session = Depends(get_db)):
    """Export questions as CSV"""
    try:
        csv_path = services.export_to_csv(db)
        return FileResponse(
            csv_path,
            media_type="text/csv",
            filename="questions_export.csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/pdf/")
def export_pdf(db: Session = Depends(get_db)):
    """Export questions as PDF"""
    try:
        pdf_path = services.export_to_pdf(db)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="questions_export.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/")
def get_status(db: Session = Depends(get_db)):
    """Get system status"""
    try:
        total_files = db.query(models.UploadedFile).count()
        processed_files = db.query(models.UploadedFile).filter(
            models.UploadedFile.status == "processed"
        ).count()
        total_questions = db.query(models.Question).count()
        
        return {
            "total_files": total_files,
            "processed_files": processed_files,
            "total_questions": total_questions,
            "status": "running"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("[INFO] Starting server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")