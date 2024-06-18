from hmpps_person_match_score.models.person_match_model import MatchingFromPerson, MatchingToPerson, PersonMatching


class TestPersonMatchModel:
    """
    Test person matching model
    """

    def test_model_populates_source_dataset(self):
        person_match_model = PersonMatching(
            matching_from=MatchingFromPerson(pnc="1234567890"),
            matching_to=[MatchingToPerson(pnc="1234567890")],
        )
        assert person_match_model.matching_from.source_dataset == "matching_from"
        assert person_match_model.matching_to[0].source_dataset == "matching_to"
