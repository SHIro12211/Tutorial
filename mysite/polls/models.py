import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'
    )

    def __str__(self):
        format= "calendario= %d-%m-%y, con hora:%H:%M"
        return self.question_text+datetime.datetime.now().strftime(format)

    def was_published_recently(self):#devuleve TRUE si y solo si la fecha de publicacion es mayor de 24h,
        # o sea que se hizo la publicacion hace mas de 24h
        #Ej: Tiene que haberse punlicado el miercoles si hoy es vieres para que sea FALSE
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        #esta es la otra opcion, que si el user pone la hora de la publicacion futura, entonces la publicacion no sera
        #reciente hasta que pase las 34h
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now#de esta forma el return no podra devolcer TRUE x
        # ayuda de la comparacion now()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
