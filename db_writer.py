import pandas as pd
from typing import List
from transformers import AutoTokenizer, TFAutoModel
from datasets import Dataset
from data_handler import DataHandler
from dotenv import load_dotenv
from typing import Tuple, Dict
import os
import pinecone
import re

'''
TAKING LOADED DATA AND WRITING TO A PINECONE VECTOR DATABASE
'''

class DBWriter:
    def __init__(self, index_name: str = 'jstor-semantic-search', path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.index_name = index_name
        self.path_to_data = path_to_data
        self.data_handler = DataHandler(self.path_to_data)
        self._load_env_vars()

    def _load_data(self) -> pd.DataFrame:
        article_data = self.data_handler.run()
        self.article_data = article_data
        return article_data

    def _load_env_vars(self) -> Tuple[str]:
        load_dotenv()
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = os.getenv("PINECONE_ENV")
        return self.PINECONE_API_KEY, self.PINECONE_ENV

    def _pinecone_init_index(self, dimensions: int = 768, metric: str ='euclidean'):
        pinecone.init(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        existing_indexes = pinecone.list_indexes()
        if len(existing_indexes) > 0:
            print("Index already found, not creating a new one") # TODO: logger with formatting
            # TODO: error handling if index mismatch
            return None
        
        pinecone.create_index(self.index_name, dimension=dimensions, metric=metric)
        index_description = pinecone.describe_index(self.index_name)
        return index_description

    def _pinecone_init_index_client(self):
        pinecone.init(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        self.pinecone_client = pinecone.Index(self.index_name)
    
    def _pinecone_insert_embeddings(self, embeddings: List):
        if not hasattr(self, "pinecone_client"):
            self._pinecone_init_index_client()
        # TODO: add metadata to be able to filter by later
        metadata = None
        self.pinecone_client.upsert(vectors = embeddings, metadata = metadata)
    
    def _pinecone_delete_index(self):
        pinecone.delete_index(self.index_name)

    # TODO: does this need to be separate?
    def _pinecone_query_index(self, query_string: str, top_n: int = 5) -> Dict:
        if not hasattr(self, "pinecone_client"):
            self._pinecone_init_index_client()
        # embed the query string with data handler
        embedded_query = self._embed_entry(query_string) # TODO: get just the list type vector from this to pass as query 
        # query the index against the embedded query
        query_result = pinecone_client.query(
            vector= embedded_query,
            top_k= top_n,
            include_values= True
            )
        return query_result

    def _create_metadata_from_df_row(self, row: pd.Series) -> Dict:
        # TODO: use this in upsert
        # TODO: when embedding, combine title and subtitle? Some articles seem to rely on subtitle for meaning and title is more catchy
        row = row.fillna("") # TODO: better way of handling nulls in columns?
        metadata = {
            "sub_title": row["subTitle"],
            "date_published" : row["datePublished"],
            "creator" : row["creator"],
            "document_type" : row["docType"],
            "document_sub_type": row["docSubType"],
            "parent_publication": row["isPartOf"],
            "url": row["url"],
            "categories": row["sourceCategory"],
            "word_count": row["wordCount"], 
            "word_count": row["wordCount"], 
            "word_count": row["wordCount"], 
            "language": row["language"],
            "page_count": row["pageCount"],
            "issue_number": row["issueNumber"],
            "volume_number": row["volumeNumber"],
            "publisher": row["publisher"]
        }
        return metadata

    def _batched_upsert(self, batch_size= 100):
        pass
        # TODO: upsert to pinecone in batches, max should be 100 at a time

    def process_row(self, row: pd.Series):
        # combine title and subtitle
        # TODO: chunk? look at title trends first?
        # TODO: preserve original title? but preprocessing is minimal...
        combined_title = " ".join([str(row["title"]), str(row["subTitle"]) if str(row["subTitle"]) not in ["NaN", "nan"] else ""])
        cleaned_title = re.sub(" +", " ", "".join(char for char in combined_title if char.isalnum() or char == " ")).strip()
        # print(f"CLEANED TITLE: {cleaned_title}")
        embedded_title = self.data_handler._embed_entry(cleaned_title)
        # print(f"EMBEDDED TITLE: {embedded_title}")
        row_metadata = self._create_metadata_from_df_row(row)
        # print(f"ROW METADATA: {row_metadata}")
        return {"title_embedding" : embedded_title, "metadata" : row_metadata}
            # TODO: batched upsert :) (back in the run method)
        
    def run(self):
        # load data as pd df self.article_data 
        self._load_data()
        # init index if not already exists
        self._pinecone_init_index()
        # init index client as self.pinecone_client
        self._pinecone_init_index_client()
        # for each row in data
        # TODO: how to store this for upsert (from process row)
        article_data.apply(self.process_row)

if __name__ == "__main__":
    # run some methods to sense check during dev
    print('reached eof')
    db_writer = DBWriter()
    db_writer._pinecone_init_index()
    data = db_writer._load_data()
    print(db_writer.process_row(data.iloc[0]))