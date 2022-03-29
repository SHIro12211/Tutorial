from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),#cuando al directorio de polls(eso es lo q significa ''), ve a views.py
    # y ejecuta la funcion index
]
