from typing_extensions import TypedDict, Literal, List
from pydantic import BaseModel, Field
from typing import Annotated
from operator import add


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

class Section(BaseModel) :
    title : str = Field(description="This is title of the section for the topic")
    description : str = Field(description="This is the brief overview of the section")

class Sections(BaseModel) :
    sections : List[Section] = Field(description="sections of the report")

class orchastratorstate(TypedDict) :
    topic : str
    sections : List[Section]
    completed_section : Annotated[list, add]
    finalreport: str

class workerstate(TypedDict) :
    section : str
    completed_section: Annotated[list, add]