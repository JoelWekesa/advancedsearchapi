from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from movies.movies import MovieId, PageParams, getMovie, getMovies
from search.search import SearchParams, get_search_results
from search.setup import add_to_db_in_batches


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return {
        "message": "API is up and running! Happy days"
    }

@app.get("/search")
async def search(params: Annotated[SearchParams, Query()]):
    return get_search_results(params)

@app.get("/movies")
async def paginatedMovies(params: Annotated[PageParams, Query()]):
    return getMovies(params)

@app.get("/movie")
async def getMovieById(params: Annotated[MovieId, Query()]):
    return getMovie(params)

@app.on_event('startup')
def startup_event():
    add_to_db_in_batches()
