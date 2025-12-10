# ai_resume_analysis
FastAPI后端服务，能够自动解析上传的简历（PDF 格式），提取关键信息（如姓名、联系方式、技能、工作经历等），并利用 AI 模型对简历进行评分和关键词匹配，帮助招聘者快速筛选候选人。

## 快速启动（本地）
```bash
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn pdfplumber redis
python app.py
```