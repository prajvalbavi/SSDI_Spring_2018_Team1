from beton.models import Bets, BetInfo, Topics, Userinfo
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import datetime
from django.db.models import Sum


class DailyBets:
    def dailybets(self):
        options = {}
        topics = {}
        bets = Bets.objects.all().filter(date_of_placing_bet = datetime.date.today()).values()
        list_of_topics = bets.values_list('topic_id_id').distinct()
        list_of_topics = [topic[0] for topic in list_of_topics]
        #import pdb
        #pdb.set_trace()
        for topic in list_of_topics:
            topic_name = Topics.objects.filter(topic_id = topic).values('topic_name')
            topics[str(topic)] = topic_name[0]['topic_name']
        return topics