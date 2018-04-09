from beton.models import Bets
from django.db.models import Sum

class BetDetails:

    def get_bet_details(self, id):
        options = {}
        option_info = Bets.objects.all().filter(topic_id_id=id).values()
        list_of_options = option_info.order_by().values_list('option').distinct()
        list_of_options = [opt[0] for opt in list_of_options]
        for opt in list_of_options:
            topics_info = option_info.filter(option = opt[0]).values()  # opt is a tuple hence opt[0]
            options[opt[0]] = dict(topics_info.aggregate(Sum('amount')), number_of_users = topics_info.count())
        return options
