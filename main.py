'''
FASTAPI APP FOR MAKING QUERIES TO VECTOR DATABASE
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

query_maker = QueryMaker()

# TODO: refactor other classes to reduce compute on each query

@app.get("/api/v1/query/{query_string}/{top_n}")
async def query_database(query_string: str, top_n: int) -> Dict:
    result = query_maker._query_index(query_string = query_string, metadata_filters = {}, top_n = top_n).to_dict()
    return result

@app.post("/api/v1/filter-query/{query_string}/{top_n}")
async def query_database_with_filters(query_string: str, metadata: Metadata, top_n: int):
    result = query_maker._query_index(query_string = query_string, metadata_filters = metadata.dict(), top_n = top_n).to_dict()
    return result

# TODO: for nicer frontend experience, pull the possible options for the discrete metadata from db?