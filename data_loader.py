import pandas as pd
from typing import List
from transformers import AutoTokenizer, TFAutoModel
from datasets import Dataset
from dotenv import load_dotenv
import os
import pinecone

'''
LOAD THE DATA INTO A DATAFRAME
'''

class DataLoader:
    def __init__(self, path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.path_to_data = path_to_data
        load_dotenv()
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = os.getenv("PINECONE_ENV")
        self._load_data()
        # self._test_pinecone_init()
        self._pinecone_init_index_client()

    def _test_pinecone_init(self):
        pinecone.init(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        pinecone.list_indexes()

    def _pinecone_init_index(self, dimensions: int =768, metric: str ='euclidean'):
        # TODO: automatically check for indexes and create new one if not already (starter project can only have one index)
        pinecone.init(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        pinecone.create_index("jstor-semantic-search", dimension=dimensions, metric=metric)
        index_description = pinecone.describe_index("jstor-semantic-search")

    def _pinecone_init_index_client(self):
        pinecone.init(api_key=self.PINECONE_API_KEY, environment=self.PINECONE_ENV)
        self.pinecone_client = pinecone.Index("jstor-semantic-search")
    
    def _pinecone_insert_embeddings(self, embeddings: List):
        if not hasattr(self, "pinecone_client"):
            self._pinecone_init_index_client()
        self.pinecone_client.upsert(embeddings)
    
    def _pinecone_delete_index(self):
        # TODO: make the index name a class prop and use throughout to make and delete
        pinecone.delete_index("jstor-semantic-search")

    def _pinecone_query_index(self, query_string: str, top_n: int = 5):
        if not hasattr(self, "pinecone_client"):
            self._pinecone_init_index_client()
        # embed the query string
        embedded_query = self.embed_entry(query_string) # TODO: get just the list type vector from this to pass as query 
        # query the index against the embedded query
        query_result = pinecone_client.query(
            vector= embedded_query,
            top_k= top_n,
            include_values= True
            )
        return query_result

    def _load_data(self):
        json_df = pd.read_json(path_or_buf=self.path_to_data, lines=True)
        self.json_df = json_df
        print(json_df.head)
        return json_df

    def _make_hf_dataset_from_data(self):
        if not hasattr(self, "json_df"):
            self._load_data()
            self._remove_columns()
        dataset = Dataset.from_pandas(self.json_df)
        self.dataset = dataset
        return dataset

    def _remove_columns(self, cols_to_remove: List[str] = 
        [
        'unigramCount', 
        'bigramCount', 
        'trigramCount', 
        'volumeNumber', 
        'pagination', 
        'outputFormat', 
        'language', 
        'pageEnd', 
        'pageStart', 
        'identifier'
        ]):
        if not hasattr(self, 'json_df'):
            self._load_data()
        new_df = self.json_df.drop(columns = cols_to_remove)
        self.json_df = new_df
        print(self.json_df)
        return new_df
    
    def _load_model(self):
        self.model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_ckpt)
        self.model = TFAutoModel.from_pretrained(self.model_ckpt, from_pt=True)
        return self.model

    def embed_entry(self, text: str):
        if not hasattr(self, 'model'):
            self._load_model()
        encoded_input = self.tokenizer(
        text, padding=True, truncation=True, return_tensors="tf"
        )
        encoded_input = {k: v for k, v in encoded_input.items()}
        model_output = self.model(**encoded_input)
        return model_output
    
    def _cleanup_data(self):
        pass
        # TODO: may or may not need depending on closer look at the data, if there's anything to drop or any text preprocessing (initial thought may need to combine multiple bits of text? e.g. check abstracts, titles, subtitles)

    def _print_data_cols(self):
        '''
        Just for own reference while developing, the columns were:
        ['datePublished', 'docSubType', 'docType', 'id', 'identifier', 'isPartOf', 'issueNumber', 'language', 'outputFormat', 'pageCount', 'pageEnd', 'pageStart', 'pagination', 'provider', 'publicationYear', 'publisher', 'sourceCategory', 'tdmCategory', 'title', 'url', 'wordCount', 'unigramCount', 'bigramCount', 'trigramCount', 'creator', 'volumeNumber', 'subTitle', 'abstract', 'doi']
        
        Could use (some of these) as further filters
        '''
        if not hasattr(self, 'json_df'):
            self._load_data()
        data_cols = self.json_df.columns.values.tolist()
        print(data_cols)
        
        return data_cols

if __name__ == "__main__":
    data_loader = DataLoader()
    data_loader._print_data_cols()
    data_loader._remove_columns()
    data_loader._load_model()
    # print(data_loader.embed_entry("testing some embedding"))
    # print(data_loader._make_hf_dataset_from_data())
    # NOTE: look into/fix NaNs in the data...
    
    # TODO: next step to load in the secrets, create pinecone index with correct dimensions and metrics, add data
