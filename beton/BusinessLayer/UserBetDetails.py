from beton.models import Bets


class UserBetDetials:

    @staticmethod
    def get_peruser_bets(username):
        print("Username in UserBetDetails", username)
        try:
            _bets = Bets.objects.filter(username=username)
            if len(_bets) == 0:
                return "success", ""
            else:
                return "success", _bets
        except Exception as e:
            return "error", str(e)
