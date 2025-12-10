from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Depends
from typing import Optional

from src.core.pdf_parser import parse_pdf_bytes
from src.core.cache import CacheClient, get_cache
from src.core.extractor import extract_key_info
from src.core.matcher import match_resume_to_job
from src.utils.cleaning import clean_text
from src.actions.api.response import UploadResponse, ExtractInfoResponse, MatchResponse, ErrorResponse
from src.actions.api.request import JobDescRequest, ExtractInfoRequest

router = APIRouter(tags=["Resume API"])

@router.post("/upload_resume", response_model=UploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_resume(file: UploadFile = File(...),
                        cache: CacheClient = Depends(get_cache)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="仅支持 PDF 文件")
    pdf_bytes = await file.read()
    parsed_text = parse_pdf_bytes(pdf_bytes)
    parsed_text = clean_text(parsed_text)
    cached_key = f"resume:{file.filename}:text"
    cached = False
    if not cache.exists(cached_key):
        cache.set(cached_key, parsed_text)
    else:
        cached = True
    return UploadResponse(filename=file.filename, parsed_text=parsed_text, cached=cached)

@router.post("/extract_info", response_model=ExtractInfoResponse, responses={404: {"model": ErrorResponse}})
async def extract_info(req: ExtractInfoRequest,
                       cache: CacheClient = Depends(get_cache)):
    key = f"resume:{req.filename}:text"
    text = cache.get_str(key)
    if not text:
        raise HTTPException(status_code=404, detail="简历未解析或缓存不存在")
    info = extract_key_info(text)
    info["raw_text"] = text
    return ExtractInfoResponse(**info)

@router.post("/match_job", response_model=MatchResponse, responses={404: {"model": ErrorResponse}})
async def match_job(req: JobDescRequest,
                    cache: CacheClient = Depends(get_cache)):
    key = f"resume:{req.filename}:text"
    text = cache.get_str(key)
    if not text:
        raise HTTPException(status_code=404, detail="简历未解析或缓存不存在")
    score, detail = match_resume_to_job(text, req.job_desc)
    return MatchResponse(filename=req.filename, job_desc=req.job_desc, match_score=score, detail=detail)
