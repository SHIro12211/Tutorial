from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(
    admin.TabularInline):  # con StackedInline defino el modelo q usare y la cantidad de modelo que muestro al inicio
    # (StackedInline) de de la misma forma que se muestra en Question
    # (TabularInline) es de forma tabla
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question text', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [
        ChoiceInline]  # con esta linea estoy anadiendo el modelo Choice y todos las que quiera al modelo Question
    list_display = ('question_text', 'pub_date', 'was_published_recently')#de esta forma hago que muestre los datos agregados como parametros
    #('_________', '_______', '___________')
    list_filter = ['pub_date', 'question_text']


admin.site.register(Question, QuestionAdmin)  # esto es la parte del costado donde aparece las opciones
