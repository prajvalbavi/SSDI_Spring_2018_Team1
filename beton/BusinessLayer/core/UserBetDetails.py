from beton.models import Bets, Topics, ClosedBets, ClosedTopics


class UserBetDetials:

    @staticmethod
    def get_peruser_bets(username):
        print("Username in UserBetDetails", username)
        try:
            _bets = Bets.objects.filter(username_id=username)
            _closedbets = ClosedBets.objects.filter(username=username)
            if len(_bets) == 0 and len(_closedbets) == 0:
                return "success", ""
            else:
                _topic_id = [b['topic_id_id'] for b in _bets.values()]
                _closed_topic_id = [b['topic_id'] for b in _closedbets.values()]

                _topics = [Topics.objects.filter(topic_id=_t).values()[0]['topic_name'] for _t in _topic_id]
                _closed_topics = [ClosedTopics.objects.filter(topic_id=_t).values()[0]['topic_name'] for _t in _closed_topic_id]
                final_bets = []
                for i,j in zip(_topics, _bets.values()):
                    j['topic_name'] = i
                    j['status'] = "Active"
                    final_bets.append(j)

                for i,j in zip(_closed_topics, _closedbets.values()):
                    j['topic_name'] = i
                    j['status'] = "Closed"
                    final_bets.append(j)
                return "success", final_bets

        except Exception as e:
            return "error", str(e)

