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
            option_info = Bets.objects.all().filter(topic_id_id=topic).values()
            list_of_options = option_info.order_by().values_list('option').distinct()
            list_of_options = [opt for opt in list_of_options]
            options = {}
            for opt in list_of_options:
                topics_info = option_info.filter(option=''.join(opt)).values()
                options[''.join(opt)] = dict(topics_info.aggregate(Sum('amount')), number_of_users=topics_info.count())
            topics[str(topic)] = dict(option=options)

        return topics