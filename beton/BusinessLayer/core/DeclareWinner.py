from beton.models import Bets, BetInfo, Topics, Userinfo, ClosedBets, ClosedTopics
import json
from django.db.models import Sum


class DeclareWinner:
    def declare_winner(self, id, option):
        if(option == "notselected"):
            return "Please select an option"
        topic = Topics.objects.filter(topic_id= id).values()
        if(topic[0]['winning_option'] != 'not declared'):
            return "You already Declared "+str(topic[0]['winning_option'])+" as winning option"
        topic.update(winning_option= option)

        ClosedTopics.objects.create(topic_id = topic[0]['topic_id'],topic_name = topic[0]['topic_name'], creator_name = topic[0]['creator_name'], start_date = topic[0]['start_date'], end_date = topic[0]['end_date'],date_of_creation = topic[0]['date_of_creation'],winning_option = topic[0]['winning_option'])
        bets = Bets.objects.filter(topic_id= id).values()
        total_amount = bets.aggregate(Sum('amount'))
        topictoclose = ClosedTopics.objects.filter(topic_id= id).values()
        topictoclose.update(total_amount=total_amount['amount__sum'])
        topictoclose.update(total_users= bets.count())
        winning_bets = Bets.objects.filter(topic_id=id, option = topic[0]['winning_option']).values()
        winning_amount = winning_bets.aggregate(Sum('amount'))
        topictoclose.update(winning_amount=winning_amount['amount__sum'])

        losing_amount = topictoclose[0]['total_amount'] - topictoclose[0]['winning_amount']
        for i in range(len(bets)):
            ClosedBets.objects.create(bet_id = bets[i]['bet_id'], topic_id = bets[i]['topic_id_id'], username = bets[i]['username_id'], option = bets[i]['option'], amount = bets[i]['amount'], date_of_placing_bet = bets[i]['date_of_placing_bet'], win = 0, win_lose_amount = 0)
            bet = ClosedBets.objects.filter(bet_id = bets[i]['bet_id']).values()
            user = Userinfo.objects.filter(username=bet[0]['username']).values()
            if(bet[0]['option'] == topictoclose[0]['winning_option']):
                bet.update(win = 1)
                amount_won_lost = bet[0]['amount']+ ((float(bet[0]['amount'])/float(topictoclose[0]['winning_amount'])) * losing_amount)
                user.update(balance=user[0]['balance'] + amount_won_lost)
            else:
                amount_won_lost = bet[0]['amount']
                user.update(balance=user[0]['balance'] - amount_won_lost)
            bet.update(win_lose_amount = amount_won_lost)
        Bets.objects.filter(topic_id=id).delete()
        BetInfo.objects.filter(topic_id=id).delete()
        Topics.objects.filter(topic_id=id).delete()
        return "Declared winner"