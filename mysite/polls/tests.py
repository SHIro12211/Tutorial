# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """Crea una pregunta con el `question_text` dado y publique el
    número dado de 'días' compensados ​​hasta ahora (negativo para preguntas publicadas
    en el pasado, positivo para preguntas que aún no se han publicado)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ Si no existen preguntas, se muestra un mensaje apropiado. """

        response = self.client.get(reverse('polls:index'))
        #si lo del primer parametro es igual al 2do
        self.assertEqual(response.status_code, 200)#si response esta en estado 200 to.do esta BIEN!!
        #si el 1er parametro contiene lo q muestra el 2do
        self.assertContains(response, "No polls are available.")#si reponse devuelve "No polls are available."
        #si el 1er parametro q es un Queryset es igual al 2do parametro que es otro Queryset
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Pregunta con una pub_date del pasado se muestran en la pagina de index
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question],)

    def test_future_question(self):
        """
        Pregunta con una pub_date del futuro se muestran en la pagina de index
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Incluso si existen preguntas pasadas y futuras, solo se muestran las preguntas pasadas
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question],)

    def test_two_past_questions(self):
        """
        La página de índice de preguntas puede mostrar varias preguntas.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)