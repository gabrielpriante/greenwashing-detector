import streamlit as st
from pathlib import Path
import pickle
import sys

# Add src/ to path so imports work
PROJECT_ROOT = Path("..").resolve()
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from text_cleaning import basic_clean_text

# Load models
@st.cache_resource
def load_keyword_detector():
    path = Path("models/keyword_detector.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_vectorizer_and_model():
    vec_path = Path("models/tfidf_vectorizer.pkl")
    model_path = Path("models/logreg_greenwash.pkl")

    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return vectorizer, model


# UI
st.title("🌱 Greenwashing Detector")
st.write("Paste any sustainability claim and detect potential greenwashing.")

claim = st.text_area("Enter sustainability claim:", height=200)

if st.button("Analyze Claim"):
    if not claim.strip():
        st.error("Please enter some text.")
    else:
        cleaned = basic_clean_text(claim)

        # Load models
        keyword_model = load_keyword_detector()
        vectorizer, logreg_model = load_vectorizer_and_model()

        # Keyword-based score
        kw_score = keyword_model(cleaned)

        # ML-based model prediction
        X_vec = vectorizer.transform([cleaned])
        prediction = logreg_model.predict(X_vec)[0]
        proba = logreg_model.predict_proba(X_vec)[0][1]

        st.subheader("🔍 Results")
        st.write(f"**Keyword Score:** {kw_score:.3f}")
        st.write(f"**ML Model Probability:** {proba:.3f}")
        st.write(f"**Final Classification:** {'⚠️ Possible Greenwashing' if prediction == 1 else '✅ Likely Honest'}")

        st.markdown("---")
        st.write("### Explanation")
        st.write("""
        - **Keyword score** shows how strongly the text matches known vague/buzzword sustainability terms.  
        - **ML probability** is from a logistic regression model trained on labeled examples.  
        - The final result is based on the ML model.
        """)
