from beton.models import Topics, BetInfo


class BetInformation:

    def _add_options(self, topic_info, option_info):
        if not 'option' in topic_info:
            topic_info['option'] = []
        topic_info['option'].append(option_info['option'])

        if not 'total_users' in topic_info:
            topic_info['total_users'] = 0
        topic_info['total_users'] += option_info['total_users']

        if not 'total_amount' in topic_info:
            topic_info['total_amount'] = 0
        topic_info['total_amount'] += option_info['total_amount']

    def _str_date(self, date):
        return date.strftime('%m/%d/%Y')

    def _get_topic_attributes(self, topic_info):
        return dict(topic_id=topic_info['topic_id'], topic_name=topic_info['topic_name'], creator_name=topic_info['creator_name_id'],start_date=self._str_date(topic_info['start_date']),
                    end_date=self._str_date(topic_info['end_date']),
                    date_of_creation=self._str_date(topic_info['date_of_creation']))

    @property
    def _add_topics(self):
        topics = {}
        for topic in Topics.objects.values():
            topic_attr = self._get_topic_attributes(topic)
            topics[topic['topic_id']] = topic_attr
        return topics

    def get_info_by_topic(self):
        bet_topics_info = self._add_topics
        topic_ids = bet_topics_info.keys()
        options_info = [BetInfo.objects.filter(topic_id_id=topic).values() for topic in topic_ids]

        for option_set in options_info:
            for option_info in option_set:
                if not option_info['topic_id_id'] in bet_topics_info:
                    bet_topics_info[option_info['topic_id_id']] = {}
                self._add_options(topic_info=bet_topics_info[option_info['topic_id_id']], option_info=option_info)

        return bet_topics_info
