'''
RE-USABLE PINECONE CLIENT CONNECTION TO PASS TO OTHER CLASSES
'''
import pinecone
import os
from dotenv import load_dotenv
from typing import Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s: %(message)s"
    )

class DBClient:
    def __init__(self, index_name: str = 'jstor-semantic-search'):
        self.index_name = index_name
        self._load_env_vars()
        self._pinecone_init()

    def _load_env_vars(self) -> Tuple[str]:
        load_dotenv()
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = os.getenv("PINECONE_ENV")
        return self.PINECONE_API_KEY, self.PINECONE_ENV

    def _pinecone_init(self):
        pinecone.init(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)

    def _init_index(self, dimensions: int = 768, metric: str ='euclidean'):
        existing_indexes = pinecone.list_indexes()
        if len(existing_indexes) > 0:
            logger.info("Index already found, not creating a new one")
            # TODO: error handling if index mismatch with existing
            return None
        
        pinecone.create_index(self.index_name, dimension=dimensions, metric=metric)
        index_description = pinecone.describe_index(self.index_name)
        return index_description

    def _init_index_client(self):
        self.pinecone_client = pinecone.Index(self.index_name)
        return self.pinecone_client

    def _delete_index(self):
        pinecone.delete_index(self.index_name)

    def run(self):
        index_init = self._init_index()
        client = self._init_index_client()
        return client, index_init