import re

def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u4e00-\u9fa5]", "", text)  # 保留常见 ASCII 与中文
    return text.strip()
