from beton.models import Bets, Topics


class UserBetDetials:

    @staticmethod
    def get_peruser_bets(username):
        print("Username in UserBetDetails", username)
        try:
            _bets = Bets.objects.filter(username_id=username)
            if len(_bets) == 0:
                return "success", ""
            else:
                _topic_id = [b['topic_id_id'] for b in _bets.values()]
                _topics = [Topics.objects.filter(topic_id=_t).values()[0]['topic_name'] for _t in _topic_id]
                final_bets = []
                for i,j in zip(_topics, _bets.values()):
                    j['topic_name'] = i
                    final_bets.append(j)
                return "success", final_bets

        except Exception as e:
            return "error", str(e)

