import re
from typing import Dict, Optional
from src.utils.regex_patterns import PHONE_PATTERN, EMAIL_PATTERN, ADDRESS_HINTS

def _extract_name(text: str) -> Optional[str]:
    # 优先匹配“姓名”提示，其次匹配英文名/中文名的常见格式
    m = re.search(r"(姓名|Name)[:：]?\s*([A-Za-z\u4e00-\u9fa5·\s]{2,30})", text)
    if m:
        return m.group(2).strip()
    # 退化策略：取第一行中看似人名的词
    first_line = text.split("\n")[0]
    m2 = re.search(r"([A-Za-z\u4e00-\u9fa5·]{2,30})", first_line)
    return m2.group(1).strip() if m2 else None

def _extract_address(text: str) -> Optional[str]:
    for hint in ADDRESS_HINTS:
        m = re.search(fr"{hint}[:：]?\s*([^\n,;，；]+)", text)
        if m:
            return m.group(1).strip()
    return None

def _extract_intent(text: str) -> Optional[str]:
    m = re.search(r"(求职意向|期望职位|目标岗位|Objective|Position)[:：]?\s*([^\n]+)", text)
    return m.group(2).strip() if m else None

def _extract_experience_years(text: str) -> Optional[float]:
    # 例如：工作经验 5 年 / 5 years experience
    m = re.search(r"(工作经验|经验|Experience)[:：]?\s*(\d+(\.\d+)?)\s*(年|years?)", text, re.IGNORECASE)
    if m:
        return float(m.group(2))
    # 通过时间跨度估算
    m2 = re.findall(r"(\d{4})\s*[-~–—]\s*(\d{4}|至今|present)", text, re.IGNORECASE)
    if m2:
        years = 0.0
        from datetime import datetime
        now_year = datetime.now().year
        for s, e in m2:
            end = now_year if re.search(r"至今|present", e, re.IGNORECASE) else int(e)
            years += max(0.0, end - int(s))
        if years > 0:
            return years
    return None

def _extract_education(text: str) -> Optional[str]:
    m = re.search(r"(学历|Education|Degree)[:：]?\s*([^\n]+)", text)
    if m:
        return m.group(2).strip()
    # 常见学位关键词
    m2 = re.search(r"(博士|硕士|本科|大专|Master|Bachelor|Ph\.?D)", text, re.IGNORECASE)
    return m2.group(0) if m2 else None

def extract_key_info(text: str) -> Dict:
    phone_m = re.search(PHONE_PATTERN, text)
    email_m = re.search(EMAIL_PATTERN, text)

    return {
        "name": _extract_name(text),
        "phone": phone_m.group(0) if phone_m else None,
        "email": email_m.group(0) if email_m else None,
        "address": _extract_address(text),
        "intent": _extract_intent(text),
        "experience_years": _extract_experience_years(text),
        "education": _extract_education(text),
    }
