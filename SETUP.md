# Semantic Job-Resume Matcher - SETUP GUIDE

Quick start guide for getting the project running.

## 1. Clone Repository
```bash
git clone https://github.com/Pranavlad51/semantic-job-resume-matcher.git
cd semantic-job-resume-matcher
```

## 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Run Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 5. Run Tests (Optional)
```bash
python run_tests.py
```

## Usage

### Option A: Load Sample Data (Recommended for demo)
1. Click "Load Sample Data" button
2. Click "Analyze Resumes"
3. Explore results

### Option B: Custom Data
1. Paste job description or upload TXT file
2. Upload resumes (PDF, DOCX, or TXT)
3. Click "Analyze Resumes"

## Features

- ✅ Semantic similarity matching
- ✅ Keyword vs semantic comparison
- ✅ Skill extraction and matching
- ✅ Detailed explanations
- ✅ Bias awareness section
- ✅ Interactive visualizations
- ✅ PDF/DOCX/TXT support

## System Requirements

- Python 3.10+
- 4GB RAM (for model)
- ~1GB disk space (for dependencies)

## Troubleshooting

### Model loading slow
- First run downloads model (~100MB)
- Subsequent runs use cache

### Memory issues
- Reduce number of resumes
- Close other applications

### PDF extraction fails
- Ensure PDF is not password-protected
- Try with a simpler PDF

## Project Structure

```
semantic-job-resume-matcher/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── SETUP.md                  # This file
│
├── src/
│   ├── __init__.py
│   ├── parser.py             # Resume text extraction
│   ├── embeddings.py         # Sentence Transformers
│   ├── similarity.py         # Cosine similarity
│   ├── skills.py             # Skill extraction
│   ├── ranking.py            # Candidate ranking
│   ├── explanation.py        # Score explanations
│   ├── comparison.py         # Semantic vs keyword
│   └── bias.py               # Bias & fairness
│
├── sample_data/
│   ├── job_description.txt
│   └── resume_*.txt          # 5 sample resumes
│
└── tests/
    ├── test_parser.py
    ├── test_similarity.py
    └── test_skills.py
```

## For Jury Presentation

1. **Load Sample Data** - Shows system works immediately
2. **Analyze** - Takes ~5-10 seconds
3. **Show Results Tab** - Candidate rankings
4. **Show Comparison Tab** - Semantic vs Keyword
5. **Show Skills Tab** - Skill matching
6. **Show Bias Tab** - Fairness considerations
7. **Show Model Info** - Technical explanation

## Next Steps

- Read README.md for detailed documentation
- Explore sample data in sample_data/ folder
- Run tests: `python run_tests.py`
- Customize for your use case

## Questions?

Refer to README.md for comprehensive FAQ and documentation.
