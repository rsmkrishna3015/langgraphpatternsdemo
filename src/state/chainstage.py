from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field


class chainstage(TypedDict):
    topic: str
    initial_story: str
    improved_story: str
    summary: str


class Router(BaseModel) :
    step : Literal["code", "explanation", "interview_question"] = Field(description="Next step in routing process") 


class Routerstate(TypedDict) :
    input : str
    decision : str
    output : str