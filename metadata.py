'''
JUST THE 'METADATA' PYDANTIC CLASS TO GIVE THE API METADATA FILTERS
'''
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class Metadata(BaseModel):
    # NOTE: using dicts of key = metadata filter type, value = corresponding filter value
    # TODO: some of these could be better to have multiple e.g. word count in range, multiple categories, can used and/or in pinecone query, look into how to do in api?
    title : Optional[Dict[str, str]] = None
    sub_title: Optional[Dict[str, str]] = None
    date_published: Optional[Dict[str, datetime]] = None
    creator: Optional[Dict[str, str]] = None
    document_type: Optional[Dict[str, str]] = None
    document_sub_type: Optional[Dict[str, str]] = None
    parent_publication: Optional[Dict[str, str]] = None
    categories: Optional[Dict[str, str]] = None
    word_count: Optional[Dict[str, int]] = None
    language: Optional[Dict[str, str]] = None
    page_count: Optional[Dict[str, int]] = None
    issue_number: Optional[Dict[str, str]] = None
    volume_number: Optional[Dict[str, str]] = None
    publisher: Optional[Dict[str, str]] = None