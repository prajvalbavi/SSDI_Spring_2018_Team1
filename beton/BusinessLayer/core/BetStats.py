from beton.models import Bets, ClosedBets
from beton.models import Userinfo
from django.db.models import Sum


class BetStats:
    def __init__(self, username):
        self.username = username
        self.WIN = 1
        self.LOSE = 0

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
        closedBets = len(ClosedBets.objects.filter(username=self.username))
        total_bets = self.get_activebets() + closedBets
        return total_bets

    def get_activebets(self):
        # Use a new table and filter it on something relevant
        activeBets = len(Bets.objects.filter(username=self.username))
        return activeBets

    def get_numberOfWins(self):
        numberOfWins = len(ClosedBets.objects.filter(username=self.username, win=self.WIN))
        return numberOfWins

    def get_totalWinAmount(self):
        totalWinAmount = ClosedBets.objects.filter(username=self.username, win=self.WIN).aggregate(Sum('amount'))
        if totalWinAmount['amount__sum'] == None:
            return 0
        else:
            return totalWinAmount['amount__sum']

    def get_numberOfLoss(self):
        numberOfLoss = len(ClosedBets.objects.filter(username=self.username, win=self.LOSE))
        return numberOfLoss

    def get_totalLossAmount(self):
        totalLossAmount = ClosedBets.objects.filter(username=self.username, win=self.LOSE).aggregate(Sum('amount'))
        if totalLossAmount['amount__sum'] == None:
            return 0
        else:
            return totalLossAmount['amount__sum']

    def get_peruser_betStats(self):
        _temp_stats = self.pack_stats()
        return _temp_stats
