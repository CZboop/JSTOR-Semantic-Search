'''
SEARCH THE DATABASE AND GET QUERY RESULTS :)
'''
from typing import Dict
from db_client import DBClient
from data_handler import DataHandler

class QueryMaker:
    def __init__(self, index_name: str = 'jstor-semantic-search', path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.index_name = index_name
        self.path_to_data = path_to_data
        self.data_handler = DataHandler(self.path_to_data)
        self.db_client = DBClient(self.index_name)

    def _query_index(self, query_string: str, top_n: int = 5, metadata_filters: Dict = {}) -> Dict:
        # TODO: how to handle different types of metadata filters and multiple at once, plus the main text query
        # TODO: would the above depend on how adding frontend? not big factor though
        if not hasattr(self, "pinecone_client"):
            self.pinecone_client = self.db_client.run()
        # embed the query string with data handler
        embedded_query = self.data_handler._embed_entry(query_string)
        # query the index against the embedded query
        query_result = self.pinecone_client.query(
            vector= embedded_query,
            top_k= top_n,
            include_values= True
            )
        return query_result

if __name__ == "__main__":
    # sense checks during dev
    query_maker = QueryMaker()
    query_result = query_maker._query_index("19th century french poetry")
    print(query_result)