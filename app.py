"""
app.py
Main Streamlit application for Semantic Job-Resume Matcher

This is the entry point for the web interface. Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Import all modules
from src.parser import extract_resume_text
from src.embeddings import load_model, generate_embedding, generate_embeddings_batch
from src.similarity import calculate_cosine_similarity, similarity_to_percentage, get_similarity_level
from src.skills import extract_skills, get_skill_summary, keyword_matching_score
from src.ranking import rank_candidates, get_ranked_candidates_summary
from src.explanation import generate_explanation, extract_experience_keywords
from src.comparison import compare_matching_methods
from src.bias import get_bias_awareness_text, get_fairness_metrics_explanation

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Semantic Job-Resume Matcher",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.3em;
        color: #555;
        margin-bottom: 30px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.model = None
    st.session_state.job_embedding = None
    st.session_state.analysis_complete = False
    st.session_state.results = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def load_sentence_transformer_model():
    """Load the model once and cache it."""
    with st.spinner("Loading Sentence Transformer model..."):
        model = load_model()
        return model

def load_sample_data():
    """Load sample data from files."""
    sample_dir = Path("sample_data")
    
    if not sample_dir.exists():
        st.error("❌ Sample data directory not found!")
        return None
    
    try:
        # Load job description
        with open(sample_dir / "job_description.txt", "r") as f:
            job_text = f.read()
        
        # Load resumes
        resumes = {}
        resume_files = sorted(sample_dir.glob("resume_*.txt"))
        
        for i, resume_file in enumerate(resume_files, 1):
            with open(resume_file, "r") as f:
                resumes[f"Candidate {i}"] = f.read()
        
        return {
            'job_description': job_text,
            'resumes': resumes
        }
    except Exception as e:
        st.error(f"❌ Error loading sample data: {str(e)}")
        return None

def perform_analysis(job_text, resumes_dict, model):
    """Perform complete semantic analysis."""
    try:
        # Generate job embedding
        job_embedding = generate_embedding(job_text, model)
        
        # Extract job skills
        job_skills = extract_skills(job_text)
        
        # Process each resume
        candidates_data = []
        resume_texts = {}
        
        for candidate_name, resume_text in resumes_dict.items():
            # Generate resume embedding
            resume_embedding = generate_embedding(resume_text, model)
            
            # Calculate semantic similarity
            semantic_similarity = calculate_cosine_similarity(job_embedding, resume_embedding)
            
            # Calculate keyword matching score
            keyword_score = keyword_matching_score(job_text, resume_text)
            
            # Extract skills
            resume_skills = extract_skills(resume_text)
            skill_summary = get_skill_summary(job_skills, resume_skills)
            
            # Store data
            candidates_data.append({
                'candidate_name': candidate_name,
                'resume_text': resume_text,
                'similarity_score': semantic_similarity,
                'similarity_percentage': similarity_to_percentage(semantic_similarity),
                'similarity_level': get_similarity_level(similarity_to_percentage(semantic_similarity)),
                'keyword_score': keyword_score,
                'matched_skills': skill_summary['matched_skills'],
                'missing_skills': skill_summary['missing_skills'],
                'extra_skills': skill_summary['extra_skills'],
                'skill_match_percentage': skill_summary['match_percentage'],
            })
            resume_texts[candidate_name] = resume_text
        
        # Rank candidates
        ranked_df = rank_candidates(candidates_data)
        
        # Generate explanations
        explanations = {}
        for idx, row in ranked_df.iterrows():
            exp = generate_explanation(
                candidate_name=row['candidate_name'],
                similarity_score=row['similarity_score'],
                matched_skills=row['matched_skills'],
                missing_skills=row['missing_skills'],
                job_text=job_text,
                resume_text=row['resume_text']
            )
            explanations[row['candidate_name']] = exp
        
        return {
            'job_text': job_text,
            'job_skills': job_skills,
            'job_embedding': job_embedding,
            'candidates_data': candidates_data,
            'ranked_df': ranked_df,
            'explanations': explanations,
            'resume_texts': resume_texts,
        }
    
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        return None

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown("<div class='main-title'>🤖 Semantic Job-Resume Matcher</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AI-powered resume ranking using semantic similarity</div>", unsafe_allow_html=True)
    
    # Disclaimer
    st.warning(
        "⚠️ **Disclaimer:** This system is a decision-support tool, not an automated hiring decision-maker. "
        "Semantic similarity may contain biases inherited from training data and should always be combined with human review."
    )
    
    # Load model
    if not st.session_state.model_loaded:
        st.session_state.model = load_sentence_transformer_model()
        st.session_state.model_loaded = True
    
    # ========================================================================
    # TABS
    # ========================================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📄 Input",
        "📊 Results",
        "📈 Comparison",
        "🎯 Skills Analysis",
        "ℹ️ Model Info",
        "⚖️ Bias & Fairness",
        "❓ FAQ"
    ])
    
    # ========================================================================
    # TAB 1: INPUT
    # ========================================================================
    
    with tab1:
        st.header("📄 Input Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Option 1: Load Sample Data")
            if st.button("📂 Load Sample Data", key="load_sample"):
                sample_data = load_sample_data()
                if sample_data:
                    st.session_state.job_text = sample_data['job_description']
                    st.session_state.resumes_dict = sample_data['resumes']
                    st.success("✅ Sample data loaded successfully!")
                    st.info(f"Loaded {len(sample_data['resumes'])} sample resumes")
        
        with col2:
            st.subheader("Option 2: Custom Data")
            st.info("Or enter/upload your own job description and resumes")
        
        st.divider()
        
        # Job Description
        st.subheader("🎯 Job Description")
        job_input_method = st.radio("How do you want to input the job description?", ["Paste Text", "Upload File"])
        
        if job_input_method == "Paste Text":
            job_text = st.text_area("Paste job description:", height=150, key="job_text_area")
        else:
            job_file = st.file_uploader("Upload job description (TXT):", type=["txt"])
            if job_file:
                job_text = job_file.read().decode('utf-8')
            else:
                job_text = ""
        
        if job_text:
            st.session_state.job_text = job_text
            st.success(f"✅ Job description loaded ({len(job_text)} characters)")
        
        st.divider()
        
        # Resumes
        st.subheader("📄 Resumes")
        st.info("Upload multiple resumes in PDF, DOCX, or TXT format")
        
        uploaded_files = st.file_uploader(
            "Upload resumes:",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        resumes_dict = {}
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    # Create temporary file
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Extract text
                    resume_text = extract_resume_text(temp_path)
                    candidate_name = uploaded_file.name.split('.')[0]
                    resumes_dict[candidate_name] = resume_text
                    
                    # Clean up
                    os.remove(temp_path)
                    st.success(f"✅ {uploaded_file.name}")
                
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            
            if resumes_dict:
                st.session_state.resumes_dict = resumes_dict
                st.info(f"Loaded {len(resumes_dict)} resumes")
        
        st.divider()
        
        # Analyze Button
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🚀 Analyze Resumes", key="analyze_btn", use_container_width=True):
                if not hasattr(st.session_state, 'job_text') or not st.session_state.job_text:
                    st.error("❌ Please provide a job description")
                elif not hasattr(st.session_state, 'resumes_dict') or not st.session_state.resumes_dict:
                    st.error("❌ Please provide at least one resume")
                else:
                    with st.spinner("🔄 Analyzing resumes..."):
                        results = perform_analysis(
                            st.session_state.job_text,
                            st.session_state.resumes_dict,
                            st.session_state.model
                        )
                        if results:
                            st.session_state.results = results
                            st.session_state.analysis_complete = True
                            st.success("✅ Analysis complete!")
    
    # ========================================================================
    # TAB 2: RESULTS
    # ========================================================================
    
    with tab2:
        st.header("📊 Candidate Rankings")
        
        if st.session_state.analysis_complete and st.session_state.results:
            results = st.session_state.results
            ranked_df = results['ranked_df']
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Candidates", len(ranked_df))
            with col2:
                best_score = ranked_df.iloc[0]['similarity_percentage']
                st.metric("Best Match", f"{best_score}%")
            with col3:
                avg_score = ranked_df['similarity_percentage'].mean()
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col4:
                worst_score = ranked_df.iloc[-1]['similarity_percentage']
                st.metric("Worst Match", f"{worst_score}%")
            
            st.divider()
            
            # Ranking Table
            st.subheader("🏆 Ranking Table")
            
            display_df = ranked_df[['rank', 'candidate_name', 'similarity_percentage', 'similarity_level', 'matched_skills', 'missing_skills']].copy()
            display_df.columns = ['Rank', 'Candidate', 'Match %', 'Level', 'Matched Skills', 'Missing Skills']
            display_df['Matched Skills'] = display_df['Matched Skills'].apply(lambda x: ', '.join(x[:3]) + ('...' if len(x) > 3 else ''))
            display_df['Missing Skills'] = display_df['Missing Skills'].apply(lambda x: ', '.join(x[:2]) + ('...' if len(x) > 2 else ''))
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Detailed explanations
            st.subheader("📝 Detailed Match Explanations")
            
            for idx, row in ranked_df.iterrows():
                candidate_name = row['candidate_name']
                similarity_pct = row['similarity_percentage']
                similarity_level = row['similarity_level']
                matched_skills = row['matched_skills']
                missing_skills = row['missing_skills']
                
                with st.expander(f"#{row['rank']} - {candidate_name} ({similarity_pct}%)"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Overall Match", f"{similarity_pct}%")
                        st.caption(similarity_level)
                    
                    with col2:
                        st.write("**✓ Matched Skills:**")
                        if matched_skills:
                            for skill in matched_skills:
                                st.write(f"  • {skill}")
                        else:
                            st.write("  None")
                    
                    with col3:
                        st.write("**✗ Missing Skills:**")
                        if missing_skills:
                            for skill in missing_skills[:5]:
                                st.write(f"  • {skill}")
                            if len(missing_skills) > 5:
                                st.write(f"  ... and {len(missing_skills) - 5} more")
                        else:
                            st.write("  All skills matched!")
                    
                    st.divider()
                    
                    # Explanation
                    exp = results['explanations'][candidate_name]
                    st.write("**Explanation:**")
                    st.write(exp['explanation'])
        else:
            st.info("👈 Please load data and click 'Analyze Resumes' to see results")
    
    # ========================================================================
    # TAB 3: COMPARISON
    # ========================================================================
    
    with tab3:
        st.header("📈 Keyword vs Semantic Matching")
        
        if st.session_state.analysis_complete and st.session_state.results:
            results = st.session_state.results
            ranked_df = results['ranked_df']
            job_text = results['job_text']
            
            st.info(
                "**Why This Matters:** Semantic matching understands meaning beyond exact words. "
                "A resume saying 'built ML systems' matches 'machine learning engineer' even though exact words differ."
            )
            
            # Comparison chart
            comparison_data = []
            for idx, row in ranked_df.iterrows():
                comparison_data.append({
                    'Candidate': row['candidate_name'],
                    'Semantic Match %': row['similarity_percentage'],
                    'Keyword Match %': row['keyword_score']
                })
            
            comp_df = pd.DataFrame(comparison_data)
            
            fig = go.Figure(data=[
                go.Bar(x=comp_df['Candidate'], y=comp_df['Semantic Match %'], name='Semantic Matching'),
                go.Bar(x=comp_df['Candidate'], y=comp_df['Keyword Match %'], name='Keyword Matching')
            ])
            fig.update_layout(
                title="Semantic vs Keyword Matching Scores",
                barmode='group',
                yaxis_title="Match Score (%)",
                xaxis_title="Candidate",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Detailed comparison for each candidate
            st.subheader("📊 Individual Comparisons")
            for idx, row in ranked_df.iterrows():
                with st.expander(f"{row['candidate_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Semantic Match", f"{row['similarity_percentage']}%", delta="Uses meaning")
                    with col2:
                        st.metric("Keyword Match", f"{row['keyword_score']}%", delta="Exact words")
                    
                    diff = row['similarity_percentage'] - row['keyword_score']
                    if abs(diff) > 5:
                        if diff > 0:
                            st.success(
                                f"✅ Semantic matching is {diff:.1f}% higher. "
                                "This candidate uses different terminology but similar concepts."
                            )
                        else:
                            st.info(
                                f"ℹ️ Keyword matching is {abs(diff):.1f}% higher. "
                                "Many exact terms match, but contexts may differ."
                            )
                    else:
                        st.info("✓ Both methods agree on this candidate.")
        else:
            st.info("👈 Please load data and click 'Analyze Resumes' to see results")
    
    # ========================================================================
    # TAB 4: SKILLS ANALYSIS
    # ========================================================================
    
    with tab4:
        st.header("🎯 Skills Analysis")
        
        if st.session_state.analysis_complete and st.session_state.results:
            results = st.session_state.results
            ranked_df = results['ranked_df']
            job_skills = results['job_skills']
            
            st.subheader(f"Required Skills ({len(job_skills)})")
            st.write(', '.join(job_skills[:10]))
            if len(job_skills) > 10:
                st.write(f"... and {len(job_skills) - 10} more")
            
            st.divider()
            
            # Skills overview
            st.subheader("🏆 Candidate Skills Overlap")
            
            skills_data = []
            for idx, row in ranked_df.iterrows():
                skills_data.append({
                    'Candidate': row['candidate_name'],
                    'Matched': len(row['matched_skills']),
                    'Missing': len(row['missing_skills']),
                })
            
            skills_df = pd.DataFrame(skills_data)
            
            fig = go.Figure(data=[
                go.Bar(x=skills_df['Candidate'], y=skills_df['Matched'], name='Matched Skills'),
                go.Bar(x=skills_df['Candidate'], y=skills_df['Missing'], name='Missing Skills')
            ])
            fig.update_layout(
                title="Skills Matched vs Missing",
                barmode='stack',
                yaxis_title="Number of Skills",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Detailed skill breakdown
            st.subheader("📋 Detailed Skills Breakdown")
            for idx, row in ranked_df.iterrows():
                with st.expander(f"{row['candidate_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Matched Skills:**")
                        if row['matched_skills']:
                            for skill in row['matched_skills']:
                                st.write(f"  ✅ {skill}")
                        else:
                            st.write("  None")
                    
                    with col2:
                        st.write("**Missing Skills:**")
                        if row['missing_skills']:
                            for skill in row['missing_skills']:
                                st.write(f"  ❌ {skill}")
                        else:
                            st.write("  All matched!")
        else:
            st.info("👈 Please load data and click 'Analyze Resumes' to see results")
    
    # ========================================================================
    # TAB 5: MODEL INFO
    # ========================================================================
    
    with tab5:
        st.header("ℹ️ How This Works")
        
        st.subheader("🧠 Understanding Semantic Embeddings")
        st.write("""
        This application uses **Sentence Transformers** to convert text into numerical vectors called **embeddings**.
        
        **Key Concept:** Texts with similar meanings are represented by vectors that are close to each other in space.
        
        **Example:**
        - "Building machine learning models" → embedding [0.5, 0.3, 0.8, ...]
        - "Developing predictive systems" → embedding [0.49, 0.31, 0.79, ...]
        - These embeddings are very similar (cosine similarity ≈ 0.95)
        
        But:
        - "JavaScript web development" → embedding [-0.2, 0.9, 0.1, ...]
        - This is very different (cosine similarity ≈ 0.15)
        """)
        
        st.divider()
        
        st.subheader("📊 The Process")
        st.markdown("""
        1. **Text Extraction** - Extract text from PDF/DOCX/TXT resumes
        2. **Embeddings** - Convert job description and resumes into vectors
        3. **Cosine Similarity** - Calculate how similar each resume is to the job
        4. **Ranking** - Sort candidates by similarity score
        5. **Skill Extraction** - Identify matching and missing technical skills
        6. **Explanation** - Generate human-readable explanations
        """)
        
        st.divider()
        
        st.subheader("🛠️ Technical Details")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Model:** all-MiniLM-L6-v2")
            st.write("**Embedding Dimension:** 384")
            st.write("**Speed:** Very fast (optimized for speed)")
            st.write("**Memory:** Lightweight (~22M parameters)")
        
        with col2:
            st.write("**Similarity Metric:** Cosine Similarity")
            st.write("**Range:** 0.0 (no match) to 1.0 (perfect match)")
            st.write("**Framework:** PyTorch + Scikit-learn")
            st.write("**Language:** English")
        
        st.divider()
        
        st.subheader("⚡ Why Cosine Similarity?")
        st.write("""
        Cosine similarity measures the angle between two vectors:
        - **1.0** = Identical direction (perfect match)
        - **0.5** = 60° angle (moderate similarity)
        - **0.0** = Perpendicular (completely different)
        
        It's robust to text length and captures semantic meaning perfectly.
        """)
    
    # ========================================================================
    # TAB 6: BIAS & FAIRNESS
    # ========================================================================
    
    with tab6:
        st.header("⚖️ Bias & Fairness")
        
        bias_info = get_bias_awareness_text()
        fairness_metrics = get_fairness_metrics_explanation()
        
        st.subheader("✅ What We Don't Use")
        st.write("This system intentionally excludes personal attributes:")
        for item in bias_info['what_we_dont_use']:
            st.write(item)
        
        st.divider()
        
        st.subheader("⚠️ Why Bias Still Matters")
        st.write("Even with sensitive attributes removed, biases can persist:")
        for item in bias_info['why_bias_still_matters']:
            st.write(item)
        
        st.divider()
        
        st.subheader("✅ Recommendations")
        for item in bias_info['recommendations']:
            st.write(item)
        
        st.divider()
        
        st.subheader("📊 Fairness Metrics to Monitor")
        for metric in fairness_metrics['metrics']:
            with st.expander(metric['name']):
                st.write(f"**Description:** {metric['description']}")
                st.write(f"**Target:** {metric['target']}")
        
        st.divider()
        
        st.subheader("⚠️ Important Disclaimer")
        st.error(bias_info['disclaimer'])
    
    # ========================================================================
    # TAB 7: FAQ
    # ========================================================================
    
    with tab7:
        st.header("❓ Frequently Asked Questions")
        
        faq_items = [
            {
                "q": "Why semantic matching over keyword matching?",
                "a": "Keyword matching misses qualified candidates using different terminology. Semantic matching understands that 'predictive models' ≈ 'machine learning models' even with different wording."
            },
            {
                "q": "Is this system biased?",
                "a": "We exclude sensitive attributes (name, gender, age), but bias can still hide in resume wording and training data. Always combine with human review."
            },
            {
                "q": "Can I use this for final hiring decisions?",
                "a": "No. This is a decision-support tool, not a decision-maker. Use it to screen resumes, but always involve human reviewers."
            },
            {
                "q": "What file formats are supported?",
                "a": "PDF (PyMuPDF), DOCX (python-docx), and TXT formats are supported."
            },
            {
                "q": "Why does the score sometimes differ from keyword matching?",
                "a": "Semantic matching understands meaning, not just words. Two resumes with similar concepts get similar scores even if wording differs."
            },
            {
                "q": "What model is used?",
                "a": "all-MiniLM-L6-v2 from Hugging Face. It's fast, accurate, and works on CPU."
            },
            {
                "q": "How long are resumes?",
                "a": "No strict limit, but very long resumes (10k+ words) may take longer. Normal resumes (500-2000 words) are fine."
            },
            {
                "q": "Does language matter?",
                "a": "The model is trained on English. Other languages may work but with reduced accuracy."
            },
        ]
        
        for i, item in enumerate(faq_items):
            with st.expander(f"Q: {item['q']}"):
                st.write(f"**A:** {item['a']}")

if __name__ == "__main__":
    main()
