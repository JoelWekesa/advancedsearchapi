import json
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field
from search.setup import data


class PageParams(BaseModel):
    page:int = Field(1, ge=1)
    limit:int = Field(1000, ge=100, le=100000)

class MovieId(BaseModel):
    id: int = Field(le=120000000)


def getMovies(params: Annotated[PageParams, Query()]):
    start =( params.page - 1) * params.limit
    end = start + params.limit

    results = data[start:end]

    response = [json.loads(result.page_content) for result in results]

    return response


def getMovie(params: Annotated[MovieId, Query()]):

    for item in data:
        if json.loads(item.page_content)['id'] == params.id:
            return json.loads(item.page_content)
        
    return None