'''
JUST THE 'QUERYSTRING' PYDANTIC CLASS TO GIVE THE API MAIN QUERY STRING
'''
from pydantic import BaseModel
from datetime import datetime

class QueryString(BaseModel):
    text: str