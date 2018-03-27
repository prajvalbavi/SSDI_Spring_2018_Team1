from beton.models import  Topics, BetInfo


class BetInformation:

    def _add_option(self, topic_info, option_info):
        if not 'option' in topic_info:
            topic_info['option'] = []
        topic_info['option'].append(option_info['option'])

        if not 'total_users' in topic_info:
            topic_info['total_users'] = 0
        topic_info['total_users'] += option_info['total_users']

        if not 'total_amount' in topic_info:
            topic_info['total_amount'] = 0
        topic_info['total_amount'] +=option_info['total_amount']



    def get_info_by_topic(self):

        bet_topics_info  = {}
        topic_ids = [x['topic_id'] for x in Topics.objects.values()]

        options_info = [BetInfo.objects.filter(topic_id_id=topic).values() for topic in topic_ids]

        for option_set in options_info:
            for option_info in option_set:
                if not option_info['topic_id_id'] in bet_topics_info:
                    bet_topics_info[option_info['topic_id_id']] = {}

                self._add_option(topic_info = bet_topics_info[option_info['topic_id_id']], option_info = option_info)

        return bet_topics_info






