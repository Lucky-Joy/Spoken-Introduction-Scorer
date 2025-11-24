import streamlit as st
from rubric_loader import load_rubric
from scorer import Scorer
from pathlib import Path
import json
import pandas as pd

st.set_page_config(page_title="Spoken Intro Scorer", layout="wide")

st.title("Spoken Introduction Scorer")
st.write("Automatically evaluates a student's spoken introduction using the rubric.")

st.header("Transcript Input")

input_mode = st.radio("Choose input method:", ["Paste text", "Upload .txt", "Use sample transcript"])

transcript_text = ""

if input_mode == "Paste text":
    transcript_text = st.text_area("Enter transcript:", height=200)

elif input_mode == "Upload .txt":
    uploaded = st.file_uploader("Upload transcript file:", type=["txt"])
    if uploaded is not None:
        transcript_text = uploaded.read().decode("utf-8")
        st.text_area("Preview:", value=transcript_text, height=200)

else:
    sample_path = Path("data/sample.txt")
    if sample_path.exists():
        transcript_text = sample_path.read_text()
        st.text_area("Sample transcript:", value=transcript_text, height=200)
    else:
        st.error("Sample file not found. Please place it at data/sample.txt")

try:
    rubric = load_rubric()
except Exception as e:
    st.error(f"Failed to load rubric: {e}")
    st.stop()

st.header("Scoring Options")
semantic_weight = st.slider("Semantic weight (vs rule-based)", 0.0, 1.0, 0.6, 0.05)

if st.button("Evaluate Transcript"):
    
    if not transcript_text.strip():
        st.error("Please enter or upload a transcript!")
        st.stop()
    
    with st.spinner("Scoring transcript..."):
        scorer = Scorer(rubric, semantic_weight=semantic_weight)
        result = scorer.score_transcript(transcript_text)

    st.header("Results")

    overall = result["overall_score"]
    st.metric("Overall Score (0–100)", f"{overall:.1f}")

    rows = []
    for c in result["criteria"]:
        rows.append({
            "Criterion": c["name"],
            "Score (0–100)": round(c["score"] * 100, 1),
            "Weight": c["weight"],
            "Keywords Found": f"{c['rule']['matched_keywords']}/{c['rule']['total_keywords']}",
            "Semantic Similarity": round(c['semantic']['similarity'], 3)
        })
    df = pd.DataFrame(rows)

    st.subheader("Per-Criterion Breakdown")
    st.dataframe(df, use_container_width=True)

    st.subheader("Detailed Feedback")
    for c in result["criteria"]:
        with st.expander(f"{c['name']} — {round(c['score']*100,1)} / 100"):
            st.write("**Description:**", c["description"])
            st.write("**Keyword Matches:**", c["rule"]["matched_keyword_list"])
            st.write("**Semantic Similarity:**", round(c["semantic"]["similarity"], 4))
            if c.get("word_count_feedback"):
                st.write("**Word Count:**", c["word_count_feedback"])

    st.subheader("Download Results")
    st.download_button(
        label="Download JSON",
        data=json.dumps(result, indent=2),
        file_name="result.json",
        mime="application/json",
    )


st.markdown("---")
st.caption("Built for Nirmaan AI Intern Case Study by Lucky Joy")