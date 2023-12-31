import pandas as pd
from typing import List
from transformers import AutoTokenizer, TFAutoModel
from datasets import Dataset
from dotenv import load_dotenv
import os
import pinecone

'''
LOAD THE DATA INTO A DATAFRAME, CREATE PINECONE INDEX AND LOAD THE DATA INTO THAT :)
'''

class DataHandler:
    def __init__(self, paths_to_data: List[str] = ['./data/lit_articles_2017-2023.jsonl', './data/lit_articles_2015-2016.jsonl'], embedding_model: str = 'sentence-transformers/multi-qa-mpnet-base-dot-v1'):
        self.paths_to_data = paths_to_data
        self.embedding_model = embedding_model

    def _load_data(self):
        json_dfs = []
        for file in self.paths_to_data:
            df = pd.read_json(path_or_buf=file, lines=True)
            json_dfs.append(df)
        json_df = pd.concat(json_dfs, ignore_index=True)
        
        self.json_df = json_df
        return json_df

    def _remove_columns(self, cols_to_remove: List[str] = 
        [
        'unigramCount', 
        'bigramCount', 
        'trigramCount', 
        'pagination', 
        'outputFormat', 
        'pageEnd', 
        'pageStart', 
        'identifier'
        ]):
        if not hasattr(self, 'json_df'):
            self._load_data()
        new_df = self.json_df.drop(columns = cols_to_remove)
        self.json_df = new_df
        # print(self.json_df)
        return new_df
    
    def _load_model(self):
        self.model_ckpt = self.embedding_model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_ckpt)
        self.model = TFAutoModel.from_pretrained(self.model_ckpt, from_pt=True)
        return self.model

    def _embed_entry(self, text: str):
        if not hasattr(self, 'model'):
            self._load_model()
        encoded_input = self.tokenizer(
        text, padding=True, truncation=True, return_tensors="tf"
        )
        encoded_input = {k: v for k, v in encoded_input.items()}
        model_output = self.model(**encoded_input)
        # NOTE: the embedding is not the only model output, getting it from the last hidden state
        embedding = model_output.last_hidden_state[:, 0].numpy()[0].tolist()
        return embedding

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

    def run(self):
        self._load_data()
        data = self._remove_columns()
        self._load_model()
        return data

if __name__ == "__main__":
    data_handler = DataHandler()
