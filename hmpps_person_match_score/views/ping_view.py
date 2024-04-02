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
        try:
            return "pong"
        except Exception as e:
            # logger(__name__).exception("Exception at ping endpoint")
            return e.args[0], 500
