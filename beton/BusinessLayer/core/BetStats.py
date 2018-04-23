from beton.models import Bets
from beton.models import Userinfo


class BetStats:

    def pack_stats(self):
        pass


    @staticmethod
    def get_peruser_betStats(username):
        _temp_stats = {}
        _temp_stats['totalBets'] = 1
        _temp_stats['activeBets'] = 0
        _temp_stats['numberOfWins'] = 1
        _temp_stats['numberOfLoss'] = 1
        _temp_stats['totalWinAmount'] = 1
        _temp_stats['totalLostAmount'] = 0
        return _temp_stats
