from beton.models import Bets, BetInfo, Topics, Userinfo
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json

class PlaceABet:
    def get_option_list(self, id):
        option_info = Bets.objects.all().filter(topic_id_id=id).values()
        options = option_info.order_by().values_list('option').distinct()
        options = [ opt[0] for opt in options]
        return options

    def place_a_bet(self, topic_id, username, option, amount):
        try:
            tpcid = Topics.objects.get(topic_id= topic_id)
            user = Userinfo.objects.get(username= username)
            Bets.objects.create(topic_id_id = tpcid.topic_id, username_id = user,option = option, amount = amount)
            bet_info = BetInfo.objects.filter(topic_id_id = tpcid.topic_id, option = option).values()
            if(len(bet_info) != 1 and len(bet_info) != 0):
                return "Error in database, multiple records exists in Betinfo"
            bet_info.update(total_users=bet_info[0]['total_users'] + 1)
            bet_info.update(total_amount=bet_info[0]['total_amount'] + long(amount))
            return "Success"
        except IndexError as e:
            BetInfo.objects.create(topic_id_id = tpcid.topic_id, option = option, total_amount = amount, total_users = 1)
            return "Success and new row inserted in BetInfo"
        except ObjectDoesNotExist as e:
            # raise e
            return "Invalid topic id/Username"
