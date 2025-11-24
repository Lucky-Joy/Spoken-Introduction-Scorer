import re
import math
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import clean_text, tokenize_words

_MODEL = None
def get_model(name="all-MiniLM-L6-v2"):
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(name)
    return _MODEL

class Scorer:
    def __init__(self, rubric, semantic_weight=0.6):
        self.rubric = rubric
        self.semantic_weight = float(semantic_weight)
        self.rule_weight = 1.0 - self.semantic_weight
        self.model = get_model()

        self.criterion_texts = [c.get("description","") for c in self.rubric]
        self.criterion_embs = None
        if any(self.criterion_texts):
            self.criterion_embs = self.model.encode(self.criterion_texts, convert_to_numpy=True)

    def score_transcript(self, text):
        raw_text = text
        cleaned = clean_text(text)
        words = tokenize_words(cleaned)
        word_count = len(words)

        transcript_emb = self.model.encode([cleaned], convert_to_numpy=True)[0]

        criteria_results = []
        total_weight = sum([c.get("weight",1.0) for c in self.rubric]) or 1.0
        weighted_sum = 0.0

        for idx, crit in enumerate(self.rubric):
            name = crit.get("name", f"criterion_{idx}")
            desc = crit.get("description","")
            weight = float(crit.get("weight",1.0))

            kw_list = crit.get("keywords", []) or []
            kw_list = [k.strip().lower() for k in kw_list if k.strip()!=""]
            matched = []
            for kw in kw_list:
                pattern = r"\\b" + re.escape(kw) + r"\\b"
                if re.search(pattern, cleaned):
                    matched.append(kw)
            total_k = len(kw_list)
            matched_k = len(matched)
            kw_ratio = (matched_k / total_k) if total_k>0 else 0.0

            min_w = crit.get("min_words", None)
            max_w = crit.get("max_words", None)
            wc_score = 1.0
            wc_feedback = None
            if min_w is not None and word_count < min_w:
                wc_score = 0.0
                wc_feedback = f"Below minimum words ({word_count} < {min_w})"
            elif max_w is not None and word_count > max_w:
                wc_score = 0.5
                wc_feedback = f"Above maximum words ({word_count} > {max_w})"
            else:
                wc_score = 1.0

            rule_score = 0.0
            if total_k>0:
                rule_score = 0.7 * kw_ratio + 0.3 * wc_score
            else:
                rule_score = wc_score

            sem_sim = 0.0
            sem_norm = 0.0
            if self.criterion_embs is not None:
                crit_emb = self.criterion_embs[idx]
                sim = cosine_similarity([crit_emb], [transcript_emb])[0][0]
                sem_sim = float(sim)
                low, high = 0.25, 0.85
                if sem_sim <= low:
                    sem_norm = 0.0
                elif sem_sim >= high:
                    sem_norm = 1.0
                else:
                    sem_norm = (sem_sim - low) / (high - low)

            combined = self.semantic_weight * sem_norm + self.rule_weight * rule_score

            criteria_results.append({
                "name": name,
                "description": desc,
                "weight": weight,
                "score": combined,  # 0-1
                "rule": {
                    "total_keywords": total_k,
                    "matched_keywords": matched_k,
                    "matched_keyword_list": matched,
                    "wc_score": wc_score,
                    "score": rule_score
                },
                "semantic": {
                    "similarity": sem_sim,
                    "normalized": sem_norm
                },
                "word_count_feedback": wc_feedback
            })

            weighted_sum += combined * weight

        overall = (weighted_sum / total_weight) * 100.0

        return {
            "overall_score": float(overall),
            "words": word_count,
            "criteria": criteria_results,
            "raw_transcript": raw_text
        }