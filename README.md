# SentimentSense - Sentiment Analysis Web Application

A full-stack sentiment analysis application built with FastAPI and React that provides real-time text sentiment analysis and batch CSV processing capabilities.

## 🌟 Features

- **Real-time Text Analysis**: Analyze sentiment of individual text inputs
- **Batch CSV Processing**: Upload CSV files for bulk sentiment analysis
- **Interactive Data Visualization**: Beautiful charts and confidence scores
- **Modern Responsive UI**: Built with Tailwind CSS and React
- **RESTful API**: FastAPI backend with comprehensive error handling
- **VADER Sentiment Analysis**: Industry-standard sentiment analysis algorithm

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.13**: Latest Python version
- **VADER Sentiment Analysis**: Valence Aware Dictionary and sEntiment Reasoner
- **Pandas**: Data manipulation and CSV processing
- **Uvicorn**: ASGI server for production deployment

### Frontend
- **React 19**: Latest React with hooks and functional components
- **Chart.js**: Interactive data visualization
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication

## 📦 Installation & Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
py -m pip install -r requirements.txt

# Start the development server
py -m uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🚀 Usage

### Text Sentiment Analysis
1. Open the application in your browser
2. Enter text in the text area
3. Click "Analyze Text"
4. View sentiment results with confidence scores and charts

### CSV Batch Processing
1. Prepare a CSV file with a "text" column
2. Upload the file using the file input
3. Click "Analyze CSV"
4. View results in the interactive table

### API Endpoints

#### Single Text Analysis
```bash
POST /analyze
Content-Type: multipart/form-data

Form data:
- text: "Your text here"
```

**Response:**
```json
{
  "text": "Your text here",
  "label": "Positive",
  "confidence": 0.85,
  "scores": {
    "pos": 0.85,
    "neu": 0.10,
    "neg": 0.05,
    "compound": 0.85
  }
}
```

#### CSV Batch Analysis
```bash
POST /analyze_csv
Content-Type: multipart/form-data

Form data:
- file: CSV file with "text" column
```

**Response:**
```json
{
  "results": [
    {
      "text": "Sample text 1",
      "label": "Positive",
      "confidence": 0.75,
      "scores": {...}
    },
    {
      "text": "Sample text 2", 
      "label": "Negative",
      "confidence": 0.60,
      "scores": {...}
    }
  ]
}
```

## 📊 Sentiment Analysis Details

The application uses VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis:

- **Positive**: compound score ≥ 0.05
- **Negative**: compound score ≤ -0.05  
- **Neutral**: compound score between -0.05 and 0.05

Confidence scores range from 0 to 1, with higher values indicating stronger sentiment.

## 🧪 Testing

### Backend Testing
```bash
# Test single text analysis
curl.exe -X POST "http://localhost:8000/analyze" -F "text=I love this amazing project!"

# Test CSV upload
curl.exe -X POST "http://localhost:8000/analyze_csv" -F "file=@test.csv"
```

### Frontend Testing
- Open `http://localhost:3000` in your browser
- Test text input functionality
- Test CSV upload functionality
- Verify responsive design on different screen sizes

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
# Development settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### CORS Configuration
The backend is configured to allow CORS for frontend development:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📁 Project Structure
```
pinnacle/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── venv/               # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── api.js          # API integration
│   │   └── index.css       # Tailwind CSS styles
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind configuration
└── README.md               # This file
```

## 🚀 Deployment

### Production Build
```bash
# Frontend production build
cd frontend
npm run build

# Backend production server
cd backend
py -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment (Optional)
```dockerfile
# Backend Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend Import Error**: Make sure to run uvicorn from the `backend` directory
2. **Frontend Tailwind CSS Error**: Ensure you're using Tailwind CSS v3.x
3. **CSV Upload Error**: Verify your CSV has a "text" column
4. **CORS Error**: Check that the backend is running and CORS is configured

### Error Codes
- `500 Internal Server Error`: Usually indicates CSV format issues
- `422 Validation Error`: Missing required form data
- `404 Not Found`: Incorrect API endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)

---

**Made with ❤️ using FastAPI & React** 