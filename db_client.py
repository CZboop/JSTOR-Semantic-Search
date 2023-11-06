'''
RE-USABLE PINECONE CLIENT CONNECTION TO PASS TO OTHER CLASSES
'''
import pinecone

# TODO: move refactor db client connection in writer and searcher to here

class DBClient:
    def __init__(self, index_name: str = ""):
        pass

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
        return self.pinecone_client

    def yield_client(self):
        pass