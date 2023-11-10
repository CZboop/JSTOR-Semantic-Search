'''
SEARCH THE DATABASE AND GET QUERY RESULTS :)
'''
from typing import Dict
from db_client import DBClient
from data_handler import DataHandler
from datetime import datetime
import time
import pinecone

class QueryMaker:
    def __init__(self, index_name: str = 'jstor-semantic-search', path_to_data: str = './data/lit_articles_2017-2023/lit_articles_2017-2023.jsonl'):
        self.index_name = index_name
        self.path_to_data = path_to_data
        self.data_handler = DataHandler(self.path_to_data)
        self.db_client = DBClient(self.index_name)

    def _convert_date_format_from_unix(self, unix_date: int):
        date_from_unix = datetime.fromtimestamp(unix_date)
        date_formatted = date_from_unix.strftime("%Y/%m/%d")
        return date_formatted

    def _convert_query_result_dates_from_unix(self, query_result: pinecone.core.client.model.query_response.QueryResponse):
        for result in query_result.matches:
            result["metadata"]["date_published"] = self._convert_date_format_from_unix(result["metadata"]["date_published"])
        return query_result

    def _convert_date_format_from_string(self, date_string: str):
        # NOTE: date str should be (yyyy or yyyy/mm or yyyy/mm/dd) and fill any missing with first month/day
        # TODO: validation?
        valid_formats = ["%Y/%m/%d", "%Y/%m", "%Y"]
        # TODO: try all but not fail until all failed...
        for frmt in valid_formats:
            # try:
            date_obj = datetime.strptime(date_string, frmt)
            date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            unix_date = int(time.mktime(date_obj.timetuple()))
            return unix_date
            # except:
            #     raise Exception("Invalid date format")
                # TODO: if invalid use some default dates?
                # TODO: let it check each format, only invalid once none met...

    def _query_index(self, query_string: str, top_n: int = 5, metadata_filters: Dict = {}) -> Dict:
        '''
        NOTE: metadata filters going for this type of structure
            {
                metadata name : {
                    operator : filter value
                }
            }
        '''
        if not hasattr(self, "pinecone_client"):
            self.pinecone_client, index_init = self.db_client.run()
        # removing None for optional metadata from api before giving to query
        if metadata_filters != {}:
            metadata_filters = {k: v for k, v in metadata_filters.items() if v is not None}
        # if date in filters, converting to a format that can be compared to other dates
        if "date_published" in metadata_filters.keys():
            metadata_filters["date_published"].update((k, self._convert_date_format_from_string(v)) for k,v in metadata_filters["date_published"].items())
        # embed the query string with data handler
        embedded_query = self.data_handler._embed_entry(query_string)
        # query the index against the embedded query
        query_result = self.pinecone_client.query(
            vector= embedded_query,
            top_k= top_n,
            # include_values= True,
            include_metadata= True,
            filter= metadata_filters
            )
        query_result_w_readable_date = self._convert_query_result_dates_from_unix(query_result)
        return query_result_w_readable_date

if __name__ == "__main__":
    # sense checks during dev
    query_maker = QueryMaker()
    query_result = query_maker._query_index("modernist poetry by women")
    # NOTE: if using euclidean distance vs other metrics be aware for interpreting score :)
    print(query_result)