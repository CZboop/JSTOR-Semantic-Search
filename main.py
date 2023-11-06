'''
FASTAPI APP FOR MAKING QUERIES TO VECTOR DATABASE
'''
from fastapi import FastAPI
from contextlib import asynccontextmanager
from query_maker import QueryMaker
from metadata import Metadata
from query_string import QueryString
import logging
from typing import Dict

logger = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s: %(funcName)s: %(levelname)s: %(message)s"
    )
    # TODO: format outputs / save logs

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: startup from running the db_writer, create index and upsert all data
    logger.info("Starting API...")
    yield

app = FastAPI(
    title = "JSTOR Semantic Search",
    description = "Semantic search API built for querying academic papers with JSTOR datasets",
    version = "0.1.0",
    lifespan = lifespan,
    )

query_maker = QueryMaker()

@app.get("/api/v1/query")
async def query_database(metadata: Metadata, query_string: QueryString) -> Dict:
    # TODO: problem (de?)-serializing metadata, may need to unpack or cast types
    result = query_maker._query_index(query_string = query_string.text, metadata_filters = dict(metadata))
    return result