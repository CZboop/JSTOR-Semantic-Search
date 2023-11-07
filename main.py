'''
FASTAPI APP FOR MAKING QUERIES TO VECTOR DATABASE
'''
from fastapi import FastAPI
from contextlib import asynccontextmanager
from query_maker import QueryMaker
from metadata import Metadata
import logging
from typing import Dict
import pinecone

logger = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s: %(funcName)s: %(levelname)s: %(message)s"
    )
    # TODO: format outputs / save logs

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: startup from running the db_writer, create index and upsert all data, load model
    logger.info("Starting API...")
    yield

app = FastAPI(
    title = "JSTOR Semantic Search",
    description = "Semantic search API built for querying academic papers with JSTOR datasets",
    version = "0.1.0",
    lifespan = lifespan,
    )

query_maker = QueryMaker()

# TODO: refactor other classes to reduce compute on each query

@app.get("/api/v1/query/{query_string}")
async def query_database(query_string: str) -> Dict:
    result = query_maker._query_index(query_string = query_string, metadata_filters = {}).to_dict()
    return result

@app.get("/api/v1/filter-query/{query_string}")
async def query_database_with_filters(query_string: str, metadata: Metadata):
    result = query_maker._query_index(query_string = query_string, metadata_filters = metadata.dict()).to_dict()
    return result