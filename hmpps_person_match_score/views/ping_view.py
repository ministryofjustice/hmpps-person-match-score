from hmpps_person_match_score.views.base_view import BaseView


class PingView(BaseView):
    """
    Ping View
    """

    ROUTE = "/ping"

    def get(self):
        """
        GET request handler
        """
        return "pong"
