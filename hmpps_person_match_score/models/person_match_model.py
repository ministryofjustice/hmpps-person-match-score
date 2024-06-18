from typing import Annotated, Optional

from annotated_types import Len
from pydantic import BaseModel


class Person(BaseModel):
    """
    Pydantic Person Model
    """

    pnc: Optional[str] = ""
    dob: Optional[str] = ""
    lastname: Optional[str] = ""
    firstname1: Optional[str] = ""
    firstname2: Optional[str] = ""
    firstname3: Optional[str] = ""
    firstname4: Optional[str] = ""
    firstname5: Optional[str] = ""


class MatchingFromPerson(Person):
    source_dataset: str = "matching_from"


class MatchingToPerson(Person):
    source_dataset: str = "matching_to"


class PersonMatching(BaseModel):
    """
    List of people to match
    """
    matching_from: MatchingFromPerson
    matching_to: Annotated[list[MatchingToPerson], Len(min_length=1, max_length=50)]
