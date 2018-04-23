from beton.models import Bets, BetInfo, Topics, Userinfo
import json

class DeclareWinner:
    def declare_winner(self, id, option):
        if(option == "notselected"):
            return "Please select an option"
        topic = Topics.objects.filter(topic_id= id).values()
        if(topic[0]['winning_option'] != 'not declared'):
            return "You already Declared "+str(topic[0]['winning_option'])+" as winning option"
        topic.update(winning_option= option)

        return "Declared winner"