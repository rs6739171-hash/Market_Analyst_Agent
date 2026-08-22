from pydantic import BaseModel

class ResearchRequest(BaseModel):
    ticker:str
    thread_id:str

class ApprovalRequest(BaseModel):
    thread_id:str
    action:str