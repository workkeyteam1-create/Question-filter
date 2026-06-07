# Question Filter System

A complete web application for students to upload PDF files, extract questions, identify duplicates, and filter results by unit, source, and repetition count.

## Features

### Backend (FastAPI + SQLite)
- **PDF Upload**: Upload multiple PDF files simultaneously
- **Text Extraction**: Extract text from PDFs using pdfplumber and PyPDF2
- **Question Extraction**: Identify questions using pattern matching
- **Duplicate Detection**: Count repeated questions across files
- **Unit Detection**: Automatically detect unit from question content
- **Filtering API**: Filter questions by unit, source, and minimum repeat count
- **Export Functionality**: Export results as CSV or PDF
- **Database**: SQLite database for storing files and questions

### Frontend (HTML + Bootstrap + JavaScript)
- **Three-Page Flow**: Upload → Processing → Results
- **Drag & Drop Upload**: Intuitive file upload interface
- **Real-time Processing**: Visual progress tracking
- **Interactive Filters**: Unit-wise, source-wise, and repeat count filters
- **Results Table**: Display questions with unit, source, and repeat count
- **Export Buttons**: Download results as CSV or PDF
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
Question Filter App/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services.py          # Business logic (PDF processing, export, etc.)
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Complete frontend application
├── uploads/                 # Directory for uploaded PDF files
└── README.md               # This file
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd "Question Filter App/backend"

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Backend Server

```bash
# From the backend directory
python main.py
```

The backend will start at `http://localhost:8000`

### 4. Access the Frontend

Open the frontend file in your browser:
- Direct file: `file:///path/to/Question Filter App/frontend/index.html`
- Or serve it with a simple HTTP server:

```bash
# From the frontend directory
python -m http.server 8080
# Then visit http://localhost:8080
```

## Usage Guide

### Step 1: Upload PDF Files
1. Open the application in your browser
2. Drag and drop PDF files or click to browse
3. Selected files will appear in the list
4. Click "Upload & Process Files"

### Step 2: Processing
- The system will show progress for:
  - Reading PDF files
  - Extracting questions
  - Finding duplicates
- Processing time depends on file size and number

### Step 3: View Results
- Table shows: Question, Unit, Source, Repeated count
- Use filters to narrow results:
  - **Unit**: Filter by detected unit (Unit 1-5)
  - **Source**: Filter by source file name
  - **Minimum Repeats**: Show questions repeated X+ times
- Export results:
  - **CSV**: Download as spreadsheet
  - **PDF**: Download as formatted report

## API Endpoints

### Backend API (`http://localhost:8000`)
- `GET /` - API status
- `POST /upload/` - Upload PDF files
- `POST /process/{file_id}` - Process a specific file
- `GET /questions/` - Get questions with filters
- `GET /units/` - Get all unique units
- `GET /sources/` - Get all unique sources
- `GET /export/csv/` - Export as CSV
- `GET /export/pdf/` - Export as PDF
- `GET /status/` - System status

## How It Works

### Question Extraction
1. **Text Extraction**: Uses pdfplumber (primary) and PyPDF2 (fallback)
2. **Pattern Matching**: Identifies questions using:
   - "Q." or "Question" prefixes
   - Numbered items (1., 2., etc.)
   - Question keywords (what, how, why, explain, describe, calculate)
3. **Cleaning**: Removes extra whitespace, adds proper punctuation

### Unit Detection
- **Unit 1**: Introduction, overview, basic, fundamental
- **Unit 2**: Perceptron, neural network, activation function, forward propagation
- **Unit 3**: Backpropagation, gradient descent, training, learning rate
- **Unit 4**: CNN, convolutional, pooling, image processing
- **Unit 5**: RNN, recurrent, LSTM, sequence
- **Unknown**: If no keywords match

### Duplicate Detection
- Exact text matching
- Increments repeat count for identical questions
- Tracks sources for each question

## Troubleshooting

### Common Issues

1. **Backend not starting**:
   - Check Python version: `python --version`
   - Ensure dependencies installed: `pip list`
   - Check port 8000 is free

2. **PDF upload fails**:
   - Ensure files are valid PDFs
   - Check file size (large files may take longer)
   - Verify uploads directory has write permissions

3. **No questions extracted**:
   - PDF may be scanned/image-based (requires OCR)
   - Try different PDF formats
   - Check if questions follow common patterns

4. **Frontend not connecting to backend**:
   - Ensure backend is running
   - Check CORS settings if accessing from different origin
   - Verify API URL in frontend JavaScript

### Development Notes

- The system uses SQLite for simplicity (no separate database server needed)
- Uploaded files are stored in `uploads/` directory
- Database file: `question_filter.db` (created automatically)
- For production, consider:
  - Using PostgreSQL or MySQL
  - Adding authentication
  - Implementing file cleanup
  - Adding rate limiting

## Sample Data

For testing, you can use PDF files containing questions like:

```
Q1. What is a perceptron?
Q2. Explain the backpropagation algorithm.
Q3. How does gradient descent work?
Q4. Describe the XOR problem.
```

## License

This project is for educational purposes. Feel free to modify and extend it for your needs.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with sample PDFs first