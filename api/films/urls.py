"""
Film domain URLs.
"""
from django.urls import path
from api.films.apis import FilmListApi, FilmDetailApi

urlpatterns = [
    path('', FilmListApi.as_view(), name='film-list'),
    path('<int:film_id>/', FilmDetailApi.as_view(), name='film-detail'),
]

