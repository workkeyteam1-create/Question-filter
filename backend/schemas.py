from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UploadedFileBase(BaseModel):
    filename: str
    original_name: str
    file_path: str
    file_size: int
    status: str

class UploadedFileCreate(UploadedFileBase):
    pass

class UploadedFile(UploadedFileBase):
    id: int
    uploaded_at: datetime
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str
    unit: Optional[str] = None
    source: str
    repeat_count: int = 1

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class QuestionFilter(BaseModel):
    unit: Optional[str] = None
    source: Optional[str] = None
    min_repeats: Optional[int] = None

class ExportRequest(BaseModel):
    format: str  # "csv" or "pdf"
    filters: Optional[QuestionFilter] = None