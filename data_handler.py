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
    def __init__(self, path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.path_to_data = path_to_data

    def _load_data(self):
        json_df = pd.read_json(path_or_buf=self.path_to_data, lines=True)
        self.json_df = json_df
        # print(json_df.head)
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
        self.model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
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
        embedding = model_output.last_hidden_state[:, 0].numpy()[0]
        return embedding

    def embed_all_entries(self):
        pass
        # TODO: embed the column to be queried in each piece of data (title?)
        # TODO: decide flow and return type eg is this before metadata creation and preserve whole entry? or just return embeddings
    
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

    def run(self):
        self._load_data()
        data = self._remove_columns()
        self._load_model()
        return data


if __name__ == "__main__":
    data_handler = DataHandler()
    # NOTE: look into/fix NaNs in some data...
