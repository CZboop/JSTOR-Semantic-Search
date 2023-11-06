import pandas as pd
from typing import List
from transformers import AutoTokenizer, TFAutoModel
from datasets import Dataset
from data_handler import DataHandler
from db_client import DBClient
from typing import Tuple, Dict
import os
import pinecone
import re
from tqdm import tqdm

'''
TAKING LOADED DATA AND WRITING TO A PINECONE VECTOR DATABASE
'''

class DBWriter:
    def __init__(self, index_name: str = 'jstor-semantic-search', path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.index_name = index_name
        self.path_to_data = path_to_data
        self.db_client = DBClient(self.index_name)
        self.data_handler = DataHandler(self.path_to_data)

    def _load_data(self) -> pd.DataFrame:
        article_data = self.data_handler.run()
        self.article_data = article_data
        return article_data

    def _create_metadata_from_df_row(self, row: pd.Series) -> Dict:
        # TODO: use this in upsert
        # TODO: when embedding, combine title and subtitle? Some articles seem to rely on subtitle for meaning and title is more catchy
        row = row.fillna("") # TODO: better way of handling nulls in columns?
        metadata = {
            "title": row["title"],
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
        if not hasattr(self, "processed_row_array"):
            raise Exception("Needs processed row array, use the run method") # TODO: better handle?
        # NOTE: upsert to pinecone in batches, max should be 100 at a time
        all_ids = [str(i + 1) for i in range(len(self.processed_row_array))]
        batched_rows = [self.processed_row_array[i:i + batch_size] for i in range(0, len(self.processed_row_array), batch_size)]
        batched_ids = [all_ids[i:i + batch_size] for i in range(0, len(all_ids), batch_size)]
        # print(batched_ids)
        for count, batch in enumerate(tqdm(batched_rows, desc="Upserting vectors in batches")):
            batched_vectors = [row["title_embedding"] for row in batch]
            batched_metadata = [row["metadata"] for row in batch]
            current_ids = batched_ids[count]
            upsert_result = self.pinecone_client.upsert(vectors = zip(current_ids, batched_vectors, batched_metadata))
            # print(upsert_result)

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
        processed_row = {"title_embedding" : embedded_title, "metadata" : row_metadata}
        self.processed_row_array.append(processed_row)
        return processed_row
        
    def run(self):
        # load data as pd df self.article_data 
        self._load_data()
        # init index if not already exists and init index client as self.pinecone_client
        self.pinecone_client = self.db_client.run()
        # for each row in data
        tqdm.pandas(desc='Applying embedding and metadata processing')
        self.processed_row_array = []
        self.article_data.progress_apply(self.process_row, axis = 1)
        self._batched_upsert()

if __name__ == "__main__":
    # run some methods to sense check during dev
    client = DBClient()
    client._delete_index()
    db_writer = DBWriter()
    db_writer.run()