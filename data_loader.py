import pandas as pd

'''
LOAD THE DATA INTO A DATAFRAME
'''

class DataLoader:
    def __init__(self, path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.path_to_data = path_to_data
        self._load_data()

    def _load_data(self):
        json_df = pd.read_json(path_or_buf=self.path_to_data, lines=True)
        self.json_df = json_df
        print(json_df.head)
        return json_df

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
