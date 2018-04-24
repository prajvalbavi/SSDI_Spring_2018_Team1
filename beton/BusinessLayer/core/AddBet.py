from beton.models import Topics, BetInfo
from django.db import transaction, IntegrityError
from datetime import datetime


class AddBet:
    @transaction.atomic
    def add_a_bet(self, topic_name, list_of_options, start_date_ts, end_date_ts, creation_date_ts):
        start = transaction.savepoint()
        try:
            start_date = datetime.fromtimestamp(float(start_date_ts)/1000.00)
            end_date = datetime.fromtimestamp(float(end_date_ts) / 1000.00)
            creation_date = datetime.fromtimestamp(float(creation_date_ts) / 1000.00)
            print("start_date", start_date, "end_date", end_date, "creation_date", creation_date)
            bet_topic = Topics.objects.create(topic_name=topic_name, creator_name="beton_admin",
                               start_date=start_date, end_date=end_date, date_of_creation=creation_date )

            topic_id = bet_topic.topic_id
            print ("topic_id", topic_id)
            for option in list_of_options:
                print (option)
                info = BetInfo.objects.create(topic_id_id=topic_id, option=option)
                info.save()
            transaction.savepoint_commit(start)
            return True, "Bet saved"
        except IntegrityError as i:
            transaction.savepoint_rollback(start)
            print (str(i))
            return False, "Could not save a bet"
        except Exception as e:
            transaction.savepoint_rollback(start)
            print(e)
            return False, "Unexpected exception, Could not save a bet"




