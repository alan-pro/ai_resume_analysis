from pydantic import BaseModel, Field

class JobDescRequest(BaseModel):
    filename: str = Field(..., description="简历文件名，用于从缓存读取解析文本")
    job_desc: str = Field(..., description="岗位描述文本")

class ExtractInfoRequest(BaseModel):
    filename: str = Field(..., description="简历文件名，用于从缓存读取解析文本")
