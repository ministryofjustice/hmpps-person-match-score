import pytest
from pydantic import ValidationError

from hmpps_person_match_score.models.person_match_model import MatchingFromPerson, MatchingToPerson, PersonMatching


class TestPersonMatchModel:
    """
    Test person matching model
    """

    def test_model_populates_source_dataset(self):
        """
        Test model populates the source dataset property accordingly
        """
        person_match_model = PersonMatching(
            matching_from=MatchingFromPerson(pnc="1234567890"),
            matching_to=[MatchingToPerson(pnc="1234567890")],
        )
        assert person_match_model.matching_from.source_dataset == "matching_from"
        assert person_match_model.matching_to[0].source_dataset == "matching_to"

    def test_model_doesnt_allows_mulitiple_records(self):
        """
        Test model allows multiple records
        """
        person_match_model = PersonMatching(
            matching_from=MatchingFromPerson(pnc="1234567890"),
            matching_to=[MatchingToPerson(pnc="1234567890")] * 20,
        )
        assert len(person_match_model.matching_to) == 20

    def test_model_doesnt_allow_more_than_limit_to_match(self):
        """
        Test model doesnt allow more than 50 records
        """
        with pytest.raises(ValidationError):
            PersonMatching(
                matching_from=MatchingFromPerson(pnc="1234567890"),
                matching_to=[MatchingToPerson(pnc="1234567890")] * 51,
            )
