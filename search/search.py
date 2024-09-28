import json
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field
from .setup import vector_store


class SearchParams(BaseModel):
    query:str = Field(..., max=150)
    k: int = Field(5, ge=5, le=1000)


def get_search_results(params: Annotated[SearchParams, Query()]):

    results = vector_store.similarity_search(
        query=params.query,
        k=params.k
    )


    response = [json.loads(result.page_content) for result in results]

    return response