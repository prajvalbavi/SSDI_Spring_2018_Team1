from beton.models import Bets
from beton.models import Userinfo


class BetStats:
    def __init__(self, username):
        self.username = username

    def pack_stats(self):
        _temp_stats = {}
        _temp_stats['totalBets'] = self.get_totalbets()
        _temp_stats['activeBets'] = self.get_activebets()
        _temp_stats['numberOfWins'] = self.get_numberOfWins()
        _temp_stats['numberOfLoss'] = self.get_numberOfLoss()
        _temp_stats['totalWinAmount'] = self.get_totalWinAmount()
        _temp_stats['totalLostAmount'] = self.get_totalLossAmount()
        return _temp_stats

    def get_totalbets(self):
        # Use a new table and filter it on something relevant
        closedBets = len(Bets.objects.filter(username=self.username))
        total_bets = self.get_activebets() + closedBets
        return total_bets

    def get_activebets(self):
        # Use a new table and filter it on something relevant
        activeBets = len(Bets.objects.filter(username=self.username))
        return activeBets

    def get_numberOfWins(self):
        # Use a new table and filter it on something relevant
        numberOfWins = len(Bets.objects.filter(username=self.username))
        return numberOfWins

    def get_totalWinAmount(self):
        # Use a new table and filter it on something relevant
        totalWinAmount = len(Bets.objects.filter(username=self.username))
        return totalWinAmount

    def get_numberOfLoss(self):
        # Use a new table and filter it on something relevant
        numberOfLoss = len(Bets.objects.filter(username=self.username))
        return numberOfLoss

    def get_totalLossAmount(self):
        # Use a new table and filter it on something relevant
        totalLossAmount = len(Bets.objects.filter(username=self.username))
        return totalLossAmount

    def get_peruser_betStats(self):
        _temp_stats = self.pack_stats()
        return _temp_stats
