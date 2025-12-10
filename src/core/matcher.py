import re
from typing import Tuple, Dict, Any, List
from collections import Counter

def _tokenize(text: str) -> List[str]:
    # 简单英文/中文分词（可替换为 jieba）
    tokens = re.findall(r"[A-Za-z]+|[\u4e00-\u9fa5]", text.lower())
    return [t for t in tokens if t.strip()]

def _keyword_score(resume_tokens: List[str], job_tokens: List[str]) -> float:
    resume_counter = Counter(resume_tokens)
    hit = sum(1 for t in job_tokens if t in resume_counter)
    return hit / max(1, len(job_tokens))

def _experience_relevance(resume_text: str, job_text: str) -> float:
    # 简单基于领域词的相关性评分
    domains = ["java", "python", "nlp", "cv", "backend", "frontend", "cloud", "aws", "aliyun", "k8s", "linux"]
    resume_hits = sum(1 for d in domains if d in resume_text.lower())
    job_hits = sum(1 for d in domains if d in job_text.lower())
    if job_hits == 0:
        return 0.5 if resume_hits > 0 else 0.0
    return min(1.0, resume_hits / job_hits)

# def match_resume_to_job(resume_text: str, job_desc: str) -> Tuple[float, Dict[str, Any]]:
#     resume_tokens = _tokenize(resume_text)
#     job_tokens = _tokenize(job_desc)
#     kw_score = _keyword_score(resume_tokens, job_tokens)
#     exp_score = _experience_relevance(resume_text, job_desc)
#     final = 0.6 * kw_score + 0.4 * exp_score
#     detail = {
#         "keyword_score": kw_score,
#         "experience_relevance": exp_score,
#         "resume_tokens_sample": resume_tokens[:50],
#         "job_tokens_sample": job_tokens[:50]
#     }
#     return final, detail

from sentence_transformers import SentenceTransformer, util

# 在模块加载时初始化模型（只加载一次）
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def match_resume_to_job(resume_text: str, job_desc: str) -> Tuple[float, Dict[str, Any]]:
    # 计算向量相似度
    embeddings = model.encode([resume_text, job_desc], convert_to_tensor=True)
    cosine_score = util.cos_sim(embeddings[0], embeddings[1]).item()

    # 保留原有关键词匹配作为辅助
    resume_tokens = _tokenize(resume_text)
    job_tokens = _tokenize(job_desc)
    kw_score = _keyword_score(resume_tokens, job_tokens)

    # 综合评分：Sentence-BERT 相似度为主，关键词匹配为辅
    final = 0.7 * cosine_score + 0.3 * kw_score
    detail = {
        "sentencebert_score": cosine_score,
        "keyword_score": kw_score,
        "resume_tokens_sample": resume_tokens[:50],
        "job_tokens_sample": job_tokens[:50]
    }
    return final, detail

