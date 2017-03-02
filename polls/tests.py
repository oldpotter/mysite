from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.core.urlresolvers import reverse


class QuestionMethodTests(TestCase):
    """
        未来的时间应该返回False
    """

    def test_was_published_recently_with_future_question(self):
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)
        self.assertEqual(future_question.was_published_recently(), False)

    """
        超过一天的时间应该返回False
    """

    def test_was_published_recently_with_old_question(self):
        old_date = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=old_date)
        self.assertEqual(old_question.was_published_recently(), False)

    """
        一天内的时间页应该返回True
    """

    def test_Was_published_recently_with_recent_question(self):
        recent_date = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=recent_date)
        self.assertEqual(recent_question.was_published_recently(), True)


"""
    创建Qustion的封装方法
"""


def create_question(question_text, days):
    question_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=question_date)


class QuestionViewTests(TestCase):
    """
    测试没有问题的情况
    """

    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '当前还没有问题')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    """
    测试过去的数据
    """

    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    """
    测试未来的数据
    """

    def test_index_view_with_a_future_question(self):
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "当前还没有问题", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    """同时测试未来和过去的数据"""

    def test_index_view_with_future_question_and_past_question(self):
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    """测试两条过去的数据"""

    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past question.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)
