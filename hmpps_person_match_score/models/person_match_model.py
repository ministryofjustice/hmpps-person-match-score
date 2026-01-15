from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel


class Person(BaseModel):
    """
    Pydantic Person Model
    """

    unique_id: str
    pnc: str | None = None
    dob: str | None = None
    lastname: str | None = None
    firstname1: str | None = None
    firstname2: str | None = None
    firstname3: str | None = None


class MatchingFromPerson(Person):
    source_dataset: str = "matching_from"


class MatchingToPerson(Person):
    source_dataset: str = "matching_to"


class PersonMatching(BaseModel):
    """
    List of people to match
    """

    matching_from: MatchingFromPerson
    matching_to: Annotated[list[MatchingToPerson], Len(min_length=1, max_length=100)]
