import pandas as pd
import os

def _find_col(df, candidates):
    for c in candidates:
        for col in df.columns:
            if c.lower() == col.lower():
                return col
    for col in df.columns:
        for c in candidates:
            if c.lower() in col.lower():
                return col
    return None

def load_rubric(path="data/rubric.xlsx"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Rubric file not found at {path}")
    df = pd.read_excel(path)
    name_col = _find_col(df, ["Criterion", "Name", "Criterion Name"])
    desc_col = _find_col(df, ["Description", "Criterion Description", "Details"])
    weight_col = _find_col(df, ["Weight", "Score Weight", "Points", "Mark"])
    keywords_col = _find_col(df, ["Keywords", "Key words", "Keyphrases"])
    min_col = _find_col(df, ["Min Words", "Min", "Min Word Limit", "MinWords"])
    max_col = _find_col(df, ["Max Words", "Max", "Max Word Limit", "MaxWords"])
    if name_col is None:
        name_col = df.columns[0]
    if desc_col is None:
        desc_col = df.columns[1] if len(df.columns)>1 else df.columns[0]
    if weight_col is None:
        df["__weight_temp__"] = 1.0
        weight_col = "__weight_temp__"

    rubric = []
    for _, row in df.iterrows():
        name = str(row.get(name_col, "")).strip()
        desc = str(row.get(desc_col, "")).strip()
        weight = float(row.get(weight_col, 1.0) or 1.0)
        keywords_raw = row.get(keywords_col, "") if keywords_col is not None else ""
        if pd.isna(keywords_raw):
            keywords_raw = ""
        keywords = [k.strip() for k in str(keywords_raw).split(",") if k.strip()!=""]
        min_w = None
        max_w = None
        try:
            if min_col is not None and not pd.isna(row.get(min_col)):
                min_w = int(row.get(min_col))
        except:
            min_w = None
        try:
            if max_col is not None and not pd.isna(row.get(max_col)):
                max_w = int(row.get(max_col))
        except:
            max_w = None

        rubric.append({
            "name": name or f"criterion_{len(rubric)+1}",
            "description": desc,
            "weight": weight,
            "keywords": keywords,
            "min_words": min_w,
            "max_words": max_w
        })
    return rubric