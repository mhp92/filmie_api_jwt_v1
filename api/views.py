from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model # If used custom user model

from rest_framework import generics, mixins, viewsets, views
from rest_framework import serializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from .pagination import (
    MovieLimitOffsetPagination,
    MoviePageNumberPagination,
    )
from .permissions import IsOwnerOrReadOnly
from . models import (
    Movies, 
    MovieWatchlist, 
    Watchlists, 
    WatchlistTest, 
    AWS_link,
    Genres,
    GenreMovie,
    Services,
    ServiceVod,
    MovieService,
    )

from . serializers import (
    AWS_linkSerializer,
    MovieSerializer, 
    MovieWatchlistSerializer, 
    WatchlistSerializer, 
    WatchlistTestSerializer, 
    UserSerializer, 
    UserCreateSerializer,
    UserLoginSerializer,
    GenresSerializer,
    GenreMovieSerializer,
    ServicesSerializer,
    ServiceVodSerializer,
    MovieServiceSerializer,
    )

from . pagination import WatchListLimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import FilterSet
from django_filters import rest_framework as filters


from itertools import chain

Users = get_user_model()

# Genre Ralated

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsOwnerOrReadOnly]


class GenreMovieViewSet(viewsets.ModelViewSet):
    queryset = GenreMovie.objects.all()
    serializer_class = GenreMovieSerializer

    def get_queryset(self):
        qs = GenreMovie.objects.all()
        query = self.request.GET.get('movie_id')
        if query is not None:
            qs = qs.filter(movie_id__iexact=query)
        return qs 


###################

class WatchlistTestFilter(FilterSet):
    movies = filters.CharFilter(method='filter_by_movies')

    class Meta:
        model = WatchlistTest
        fields = ('title', 'movies', )

    def filter_by_movies(self, queryset, name, value):
        movies_titles = value.strip().split(',')
        movies = Movies.objects.filter(title__in=movies_titles)
        return queryset.filter(movies__in=movies)

class WatchlistTestViewSet(viewsets.ModelViewSet):
    queryset = WatchlistTest.objects.all()
    serializer_class = WatchlistTestSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('title', 'movies__release_year', )
    # filter_class = WatchlistTestFilter


    def get_queryset(self):
        qs = WatchlistTest.objects.all()
        query = self.request.GET.get('user_id')
        if query is not None:
            qs = qs.filter(user_id__icontains=query)
        return qs 

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Users.objects.all()
        query = self.request.GET.get('username')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs 


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = Users.objects.all()



class UserLoginAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data #posted data 
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



###### VoD related

class ServicesViewSet(viewsets.ModelViewSet):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()


class ServiceVodViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceVodSerializer
    queryset = ServiceVod.objects.all()

class MovieServiceViewSet(viewsets.ModelViewSet):
    serializer_class = MovieServiceSerializer
    queryset = MovieService.objects.all()








# router/ & api/ doing the same 

############### using router and viewsets ###############

class AWS_linkViewSet(viewsets.ModelViewSet):
    queryset = AWS_link.objects.all()
    serializer_class = AWS_linkSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = AWS_link.objects.all()
        query = self.request.GET.get('title')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs 






class MovieFilter (FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    genre = filters.CharFilter(method='filter_by_genre')

    class Meta:
        model = Movies
        fields = ['title', 'genre',]
 
    def filter_by_genre(self, queryset, name, value):
        genre_names = value.strip().split(',')
        genres = Genres.objects.filter(name__in=genre_names)
        return queryset.filter(movie_genre__in=genres)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = MoviePageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filter_fields = ('title', 'genres__name')
    filter_class = MovieFilter
    ordering_fields = ('release_year',)
    search_fields = ('title',)

    

    @action(detail=True, methods=['GET'])
    def genres (self, request, pk=None):
    
        movie = get_object_or_404(Movies, id=pk)
        
        genre_ids = GenreMovie.objects.values_list('genre_id', flat=True).filter(movie_id=pk)
        
        genres = Genres.objects.filter(id__in=genre_ids)

        serializer = GenresSerializer(genres, many=True)
        return Response(serializer.data, status=HTTP_200_OK)




class MovieWatchlistViewSet(viewsets.ModelViewSet):
    queryset = MovieWatchlist.objects.all()
    serializer_class = MovieWatchlistSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = MovieWatchlist.objects.all()
        query = self.request.GET.get('watchlist_id')
        if query is not None:
            qs = qs.filter(watchlist_id__exact=query)
        return qs 


# Custom ViewSet

# class WatchlistViewSet(viewsets.ViewSet):

#     def list(self, request):
#         queryset = Watchlists.objects.all()
#         serializer = WatchlistSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def get_queryset(self):
#         qs = Watchlists.objects.all()
#         query = self.request.GET.get('type_id')
#         if query is not None:
#             qs = qs.filter(type_id__exact=query)
#         return qs 


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlists.objects.all()
    serializer_class = WatchlistSerializer
    # pagination_class = WatchListLimitOffsetPagination # see pagination.py
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication] see youtube watchlist DRF Authentication

    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('owner__username', )



    def get_queryset(self):
        qs = Watchlists.objects.all()
        query = self.request.GET.get('type_id')
        if query is not None:
            qs = qs.filter(type_id__exact=query)
        return qs 

    # assing request.user to new created watchlist
    # it works! user_id in watchlist is assigned by the logged in user, but filmie account is not connected now 
    def perform_create(self, serializer):

        user_id = self.request.user.id

        serializer.save(user_id=user_id)



    @action(detail=True, methods=['GET'])
    def movies (self, request, pk=None):
    
        watch_list = get_object_or_404(Watchlists, id=pk)
        
        movie_ids = MovieWatchlist.objects.values_list('movie_id', flat=True).filter(watchlist_id=pk)
        
        movies = Movies.objects.filter(id__in=movie_ids)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    @action(detail=True, methods=['GET'])
    def owner (self, request, pk=None):
        
        watch_list = get_object_or_404(Watchlists, id=pk)
        user_id = watch_list.user_id
        
        owner = Users.objects.filter(id=user_id)

        serializer = UserSerializer(owner, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
        





############### using generics and mixins ###############




# class MovieAPIView(mixins.CreateModelMixin, generics.ListAPIView):
#     lookup_field        = 'pk'
#     serializer_class    = MovieSerializer 



#     # we can use the search function to find everything with the type_id=2 for Movies created by users

#     def get_queryset(self):
#         qs = Movies.objects.all()
#         query = self.request.GET.get('title')
#         if query is not None:
#             qs = qs.filter(title__icontains=query)
#         return qs 


#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



# class MovieRudView(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field        = 'pk'
#     serializer_class    = MovieSerializer 

#     def get_queryset(self):
#         return Movies.objects.all()





# class MovieWatchlistAPIView(mixins.CreateModelMixin, generics.ListAPIView):
#     lookup_field        = 'pk'
#     serializer_class    = MovieWatchlistSerializer 



#     # we can use the search function to find everything with the type_id=2 for Movies created by users

#     def get_queryset(self):
#         qs = MovieWatchlist.objects.all()
#         query = self.request.GET.get('watchlist_id')
#         if query is not None:
#             qs = qs.filter(watchlist_id__exact=query)
#         return qs 


#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



# class MovieWatchlistRudView(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field        = 'pk'
#     serializer_class    = MovieWatchlistSerializer 

#     def get_queryset(self):
#         return MovieWatchlist.objects.all()






# class WatchlistAPIView(mixins.CreateModelMixin, generics.ListAPIView):
#     lookup_field        = 'pk'
#     serializer_class    = WatchlistSerializer 



#     # we can use the search function to find everything with the type_id=2 for Watchlists created by users

#     def get_queryset(self):
#         qs = Watchlists.objects.all()
#         query = self.request.GET.get('type_id')
#         if query is not None:
#             qs = qs.filter(type_id__exact=query)
#         return qs 


#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     # def perform_create(self, serializer):

#     #     user_id = self.request.user.id

#     #     serializer.save(user_id=user_id)


#     # def perform_create(self, serializer):
#     #     serializer.save(user_id=self.request.user)



# class WatchlistRudView(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field        = 'pk'
#     serializer_class    = WatchlistSerializer 




#     def get_queryset(self):
#         return Watchlists.objects.all()
