from django.urls import path
from .views import GenerateGameLinkView

urlpatterns = [
    path('generate/link', GenerateGameLinkView.as_view(), name='generate-game-link')
]
