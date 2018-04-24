from beton.models import Topics


class AdminGetTopics:
    @staticmethod
    def get_topics(date_today):
        try:
            topicList = Topics.objects.all()
            list_of_topics = [topic['topic_name'] for topic in topicList.values() if topic['date_of_creation'] == date_today]
            return "success", list_of_topics
        except Exception as e:
            return "error", str(e)

