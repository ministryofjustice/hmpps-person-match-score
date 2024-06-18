from typing import List, Optional

from pydantic import BaseModel

from hmpps_person_match_score.views.base_view import BaseView


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
    matching_to: List[MatchingToPerson]


class PersonMatchView(BaseView):
    """
    Match View
    """

    ROUTE = "/person/match"

    def post(self):
        """
        POST request handler
        """
        message = self.validate(model=PersonMatching)

        return message.model_dump_json()

    def match(self):
        """
        Link records
        """
        # row_1 = data[data["source_dataset"] == data["source_dataset"].unique()[0]]
        # row_2 = data[data["source_dataset"] == data["source_dataset"].unique()[1]]

        # # Important to impose explicit schema - otherwise where a column contains only
        # # None DuckDB will have no way of knowing it's a nullable string column
        # row_arrow_1 = pa.Table.from_pandas(row_1, schema=self.SCHEMA, preserve_index=False)
        # row_arrow_2 = pa.Table.from_pandas(row_2, schema=self.SCHEMA, preserve_index=False)
        # # Set up DuckDB linker
        # linker = DuckDBLinker(
        #     [row_arrow_1, row_arrow_2],
        #     input_table_aliases=[
        #         data["source_dataset"].unique()[0],
        #         data["source_dataset"].unique()[1],
        #     ],
        #     connection=self.duckdb_connection,
        # )
        # linker.load_settings(self.get_model_path())

        # # Make predictions
        # json_output = linker.predict().as_pandas_dataframe().to_json()

        # # Return
        # return json.loads(json_output)

