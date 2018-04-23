from beton.models import Bets, BetInfo, Topics, Userinfo
import json

class FetchBalance:
    def fetch_balance(self, username):
        user = Userinfo.objects.filter(username = username).values()
        return user[0]['balance']