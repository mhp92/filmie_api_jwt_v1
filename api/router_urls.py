from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('movie', views.MovieViewSet)
router.register('movie_watchlist', views.MovieWatchlistViewSet)
router.register('watchlist', views.WatchlistViewSet, base_name='watchlist')
router.register('watchlist_test', views.WatchlistTestViewSet)
router.register('user', views.UserViewSet)
router.register('aws_link', views.AWS_linkViewSet)
router.register('Genres', views.GenresViewSet)
router.register('GenreMovie', views.GenreMovieViewSet)
router.register('Services', views.ServicesViewSet)
router.register('ServiceVod', views.ServiceVodViewSet)
router.register('MovieService', views.MovieServiceViewSet)


urlpatterns = [
    path('', include(router.urls))
]
