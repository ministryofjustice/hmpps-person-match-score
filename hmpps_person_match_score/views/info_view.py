import os

from hmpps_person_match_score.views.base_view import BaseView


class InfoView(BaseView):
    """
    Info View
    """

    ROUTE = "/info"

    def get(self):
        """
        GET request handler
        """
        APP_BUILD_NUMBER = os.environ.get("APP_BUILD_NUMBER", "unknown")
        APP_GIT_REF = os.environ.get("APP_GIT_REF", "unknown")
        APP_GIT_BRANCH = os.environ.get("APP_GIT_BRANCH", "unknown")
        return dict(
            version=APP_BUILD_NUMBER,
            commit_id=APP_GIT_REF,
            branch=APP_GIT_BRANCH,
        )
