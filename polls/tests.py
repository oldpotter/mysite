from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question

class QuestionMethodTests(TestCase):
    """
        未来的时间应该返回False
    """
    def test_was_published_recently_with_future_question(self):
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)
        self.assertEqual(future_question.was_published_recently(),False)

    """
        超过一天的时间应该返回False
    """
    def test_was_published_recently_with_old_question(self):
        old_date = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=old_date)
        self.assertEqual(old_question.was_published_recently(),False)

    """
        一天内的时间页应该返回True
    """
    def test_Was_published_recently_with_recent_question(self):
        recent_date = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=recent_date)
        self.assertEqual(recent_question.was_published_recently(),True)
