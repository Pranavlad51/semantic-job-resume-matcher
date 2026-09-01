# Semantic Job-Resume Matcher - INSTALLATION & DEPENDENCIES

## System Requirements

- **Python:** 3.10 or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** ~2GB (for dependencies and model cache)
- **OS:** Windows, macOS, or Linux

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Pranavlad51/semantic-job-resume-matcher.git
cd semantic-job-resume-matcher
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\\Scripts\\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **streamlit** - Web interface
- **sentence-transformers** - Semantic embeddings
- **torch** - Deep learning backend
- **scikit-learn** - Similarity calculations
- **pandas** - Data handling
- **numpy** - Numerical operations
- **plotly/matplotlib** - Visualizations
- **PyMuPDF** - PDF parsing
- **python-docx** - DOCX parsing

### 4. Verify Installation

```bash
python -c "import streamlit; import torch; import sentence_transformers; print('✅ All packages installed!')"
```

## Running the Application

### Start the App

```bash
streamlit run app.py
```

The application will:
1. Download the Sentence Transformers model (~100MB) on first run
2. Cache it for subsequent runs
3. Open in your default browser at `http://localhost:8501`

### Run Tests

```bash
python -m pytest tests/ -v
```

Or using the provided script:
```bash
python run_tests.py
```

## Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution:** Make sure your virtual environment is activated and requirements installed
```bash
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```

### Issue: Model download is very slow
**Solution:** First run downloads the model. Subsequent runs use cache. Try:
```bash
pip install --upgrade sentence-transformers
```

### Issue: PDF extraction fails
**Solution:** Try converting PDF to image format or use DOCX/TXT instead

### Issue: Out of memory
**Solution:** 
- Reduce number of resumes
- Close other applications
- Restart Python process

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

## GPU Acceleration (Optional)

If you have an NVIDIA GPU:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

This speeds up embedding generation significantly.

## Offline Usage

After first run, the model is cached. You can use the app offline:
1. First run requires internet (to download model)
2. Subsequent runs work without internet

## Docker Setup (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

Build and run:
```bash
docker build -t semantic-matcher .
docker run -p 8501:8501 semantic-matcher
```

## Next Steps

1. Read **SETUP.md** for quick start
2. Read **README.md** for full documentation
3. Explore `sample_data/` folder
4. Try the web interface

## Support

For issues, check:
- README.md FAQ section
- GitHub Issues
- Troubleshooting section above
