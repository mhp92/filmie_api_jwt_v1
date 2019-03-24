from django.urls import path, include
from .views import UserCreateAPIView, UserLoginAPIView
#from . views import MovieRudView, MovieAPIView, MovieWatchlistRudView, MovieWatchlistAPIView, WatchlistRudView, WatchlistAPIView

app_name = "api"

urlpatterns = [

    path('register/', UserCreateAPIView.as_view(), name="register"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('auth/', include('rest_auth.urls')),
    # path('watchlist/', WatchlistAPIView.as_view(), name="watchlist_create"),
    # path('watchlist/<int:pk>/', WatchlistRudView.as_view(), name="watchlist_rud"),
    # path('movie/', MovieAPIView.as_view(), name="movie_create"),
    # path('movie/<int:pk>/', MovieRudView.as_view(), name="movie_rud"),
    # path('movie_watchlist/', MovieWatchlistAPIView.as_view(), name="movie_watchlist_create"),
    # path('movie_watchlist/<int:pk>/', MovieWatchlistRudView.as_view(), name="movie_watchlist_rud"),

]
