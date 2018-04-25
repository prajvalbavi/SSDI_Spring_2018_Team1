from beton.models import BetInfo

class Options:

    def options(self, id):
        options = {}
        option_info = BetInfo.objects.all().filter(topic_id_id=id).values()
        list_of_options = option_info.order_by().values_list('option').distinct()
        list_of_options = [opt for opt in list_of_options]
        for opt in list_of_options:
            options[''.join(opt)] = dict()
        return options
