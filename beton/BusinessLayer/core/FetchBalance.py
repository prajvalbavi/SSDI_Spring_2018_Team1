from beton.models import Bets, BetInfo, Topics, Userinfo
import json

class FetchBalance:
    def fetch_balance(self, username):
        user = Userinfo.objects.filter(username = username).values()
        return user[0]['balance']

    def topup_balance(self, username, amount):
        try:
            user = Userinfo.objects.get(username = username)
            user.balance = amount
            user.save()
            return "success", "Payment Successful :) Happy Betting :)"
        except Exception:
            print("Fetch Balance Expection while topup_balance")
            return "error", "Payment Updation failure"
