'''
SEARCH THE DATABASE AND GET QUERY RESULTS :)
'''
from typing import Dict

class Searcher:
    def __init__(self):
        self.db_client = DBClient()

    def make_query(self, query_string: str, metadata_filters: Dict) -> Dict:
        pass
        # TODO: how to handle different types of metadata filters and multiple at once, plus the main text query
        # TODO: would the above depend on how adding frontend? not big factor though

if __name__ == "__main__":
    pass