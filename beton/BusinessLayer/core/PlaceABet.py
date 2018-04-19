from beton.models import Bets, BetInfo, Topics, Userinfo
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from django.db.models import Sum


class PlaceABet:
    def get_option_list(self, id):
        options = {}
        option_info = Bets.objects.all().filter(topic_id_id=id).values()
        list_of_options = option_info.order_by().values_list('option').distinct()
        list_of_options = [''.join(opt) for opt in list_of_options]
        return list_of_options

    def place_a_bet(self, topic_id, username, option, amount):
        try:
            if (option == 'notselected'):
                return "Please select an Option"
            if(int(amount) <= 0):
                return "Invalid Amount"
            tpcid = Topics.objects.get(topic_id= topic_id)
            user = Userinfo.objects.filter(username= username).values()
            user1 = Userinfo.objects.get(username= username)
            bet = Bets.objects.filter(topic_id=tpcid.topic_id, username_id=user1).values()
            if(int(amount)>int(user[0]['balance'])):
                return "Insufficient balance in your account"
            if(len(bet) != 0):
                return "You have already placed a Bet on this topic!"
            Bets.objects.create(topic_id_id = tpcid.topic_id, username_id = user1,option = option, amount = amount)
            bet_info = BetInfo.objects.filter(topic_id_id = tpcid.topic_id, option = option).values()
            if(len(bet_info) != 1 and len(bet_info) != 0):
                return "Error in database, multiple records exists in Betinfo"
            bet_info.update(total_users=bet_info[0]['total_users'] + 1)
            bet_info.update(total_amount=bet_info[0]['total_amount'] + int(amount))
            user.update(balance=user[0]['balance'] - int(amount))
            return "Success"
        except IndexError as e:
            BetInfo.objects.create(topic_id_id = tpcid.topic_id, option = option, total_amount = amount, total_users = 1)
            user.update(balance=user[0]['balance'] - int(amount))
            return "Success and new row inserted in BetInfo"
        except ObjectDoesNotExist as e:
            # raise e
            return "Invalid topic id/Username"
        except ValueError as e:
            return "Invalid Amount"
