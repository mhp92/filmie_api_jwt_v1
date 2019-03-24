from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model


from django.shortcuts import get_object_or_404

Users = get_user_model()

# Create your models here.


class AccountUserPreferredGenres(models.Model):
    user_id = models.IntegerField()
    genre_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account_user_preferred_genres'


class AccountsFriendslist(models.Model):
    owner = models.ForeignKey('AuthUser', models.DO_NOTHING)
    title = models.CharField(max_length=225)

    class Meta:
        managed = False
        db_table = 'accounts_friendslist'


class AccountsFriendslistFriends(models.Model):
    friendslist = models.ForeignKey(AccountsFriendslist, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_friendslist_friends'
        unique_together = (('friendslist', 'user'),)


class AccountsProfile(models.Model):
    image = models.CharField(max_length=100)
    owner = models.OneToOneField('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_profile'


class AnalyticsCardsRoot(models.Model):
    type_id = models.IntegerField()
    sender_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    time_viewed = models.DateTimeField(blank=True, null=True)
    clicked = models.BooleanField(blank=True, null=True)
    clicked_time = models.DateTimeField(blank=True, null=True)
    eventfeed_item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analytics_cards_root'


class AnalyticsCardsTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'analytics_cards_types'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ChannelStreaming(models.Model):
    streaming_channel_name = models.CharField(max_length=255)
    link_prefix = models.CharField(max_length=255)
    link_listing = models.CharField(max_length=255)
    api = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'channel_streaming'


class ChannelUser(models.Model):
    channel_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'channel_user'


class Channels(models.Model):
    name = models.CharField(max_length=255)
    icon_path = models.CharField(max_length=255, blank=True, null=True)
    channel_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channels'


class CompareLists(models.Model):
    user_1_id = models.IntegerField()
    user_2_id = models.IntegerField()
    user_1_list_id = models.IntegerField()
    user_2_list_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'compare_lists'


class Countries(models.Model):
    name = models.CharField(max_length=255)
    reference_key = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'countries'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EngineScores(models.Model):
    engine_id = models.IntegerField()
    user_id = models.IntegerField()
    score = models.FloatField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_scores'


class EngineUser(models.Model):
    id = models.IntegerField(primary_key=True)
    engine_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_user'


class EngineUserRunlogs(models.Model):
    id = models.IntegerField(primary_key=True)
    engine_user_id = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_user_runlogs'


class EventCardTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_card_types'


class EventfeedItems(models.Model):
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventfeed_items'


class EventfeedPool(models.Model):
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventfeed_pool'


class Events(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    path = models.CharField(max_length=128)
    media = models.CharField(max_length=128, blank=True, null=True)
    relation_table = models.CharField(max_length=32, blank=True, null=True)
    relation_table_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    card_template_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class EventsShow(models.Model):
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events_show'


class FriendRecommendationResponse(models.Model):
    recommendation_id = models.IntegerField()
    sender_id = models.IntegerField()
    recipient_id = models.IntegerField()
    message = models.TextField()
    seen = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friend_recommendation_response'


class FriendToFriendRecommendations(models.Model):
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
    movie_id = models.IntegerField()
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friend_to_friend_recommendations'


class Friends(models.Model):
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
    accepted = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friends'


class GenreMovie(models.Model):
    movie_id = models.IntegerField(blank=True, null=True)
    genre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre_movie'


class Genres(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tmdb_genre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres'

    def __str__(self):
        return self.name


class Imdbkeywords(models.Model):
    imdb_kw_id = models.IntegerField()
    imdb_keyword = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'imdbkeywords'


class IpaddressTemp(models.Model):
    address = models.CharField(max_length=64)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipaddress_temp'


class KeywordMovie(models.Model):
    keyword = models.ForeignKey('Keywords', models.DO_NOTHING)
    movie_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'keyword_movie'


class Keywords(models.Model):
    keyword = models.CharField(max_length=255)
    tmdb_key_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


class ListPolling(models.Model):
    list_id = models.IntegerField()
    movie_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    vote = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'list_polling'


class ListPollingAnonymousCookies(models.Model):
    list_polling_id = models.IntegerField()
    cookie = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'list_polling_anonymous_cookies'


class ListSlug(models.Model):
    list_id = models.IntegerField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'list_slug'


class LogClones(models.Model):
    user_id = models.IntegerField()
    origin_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_clones'


class LogReportTrailer(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_report_trailer'


class LogSearchRequests(models.Model):
    user_id = models.IntegerField()
    search_request = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_search_requests'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Moods(models.Model):
    name = models.CharField(max_length=31)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moods'


class MovieChannel(models.Model):
    movie_id = models.IntegerField()
    channel_id = models.IntegerField()
    show_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'movie_channel'


class MovieEvent(models.Model):
    movie_id = models.IntegerField()
    event_date = models.DateTimeField()
    movie_event_type_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_event'


class MovieEventTypes(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'movie_event_types'


class MovieImdbKeywords(models.Model):
    filmie_id = models.IntegerField(blank=True, null=True)
    tmdb_movie_id = models.IntegerField(blank=True, null=True)
    imdb_movie_id = models.IntegerField(blank=True, null=True)
    imdb_kw_id = models.IntegerField(blank=True, null=True)
    relevance_yes = models.IntegerField(blank=True, null=True)
    relevance_total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_imdb_keywords'


class MovieMood(models.Model):
    mood = models.ForeignKey(Moods, models.DO_NOTHING)
    movie_id = models.IntegerField()
    source = models.ForeignKey('MovieMoodSource', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_mood'


class MovieMoodSource(models.Model):
    registered = models.BooleanField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_mood_source'


class MovieOrderListing(models.Model):
    rating_movie_id = models.IntegerField(blank=True, null=True)
    release_movie_id = models.IntegerField(blank=True, null=True)
    occurrence_movie_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_order_listing'


class MoviePerson(models.Model):
    movie_id = models.IntegerField()
    person_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'movie_person'


class MovieRatings(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_ratings'


class MovieService(models.Model):
    movie_id = models.IntegerField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)
    show_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_service'


class MovieServiceOld(models.Model):
    movie_id = models.IntegerField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)
    show_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_service_old'


class MovieServiceUrl(models.Model):
    movie_id = models.IntegerField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_service_url'


class MovieStream(models.Model):
    movie_id = models.IntegerField()
    streaming_channel_id = models.IntegerField()
    link = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    quality = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'movie_stream'

################# test ##################

# class MovieWatchlistManager(models.Manager):

#     def get_queryset(self):
#         return super().get_queryset()

#     def movie_from_watch_list(self):
#         return super().filter(watchlist_id=)



class MovieWatchlist(models.Model):
    movie_id = models.IntegerField()
    watchlist_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_watchlist'

    

class Movies(models.Model):
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    tmdb_id = models.IntegerField(blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)
    adult = models.BooleanField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    release_month = models.IntegerField(blank=True, null=True)
    release_day = models.IntegerField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    revenue = models.BigIntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    poster_image_path = models.CharField(max_length=255, blank=True, null=True)
    original_language = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    movie_genre = models.ManyToManyField(Genres)

    class Meta:
        managed = True
        db_table = 'movies'

    def small_poster_url(self):

        return 'https://filmie-storage.s3.eu-central-1.amazonaws.com/movie-posters/' + 'w175/' + self.poster_image_path
        

    def medium_poster_url(self):

        return 'https://filmie-storage.s3.eu-central-1.amazonaws.com/movie-posters/' + 'w300/' + self.poster_image_path
        
    
    def original_poster_url(self):

        return 'https://filmie-storage.s3.eu-central-1.amazonaws.com/movie-posters/' + 'original/' + self.poster_image_path
        

    def __str__(self):
        return '%s (%s)' % (self.title, self.release_year)

    @property   
    def genres(self):
        
        movie = get_object_or_404(Movies, id=self.pk)

        genre_ids = GenreMovie.objects.values_list('genre_id', flat=True).filter(movie_id=self.pk)

        genres = Genres.objects.filter(id__in=genre_ids)
        
        return genres

# class MoviesAddOns(Movies):
#     genre = models.ManyToManyField(Genres)

#     def __str__(self):
#         return '%s' % (self.genre)



class MoviesCast(models.Model):
    person_role_id = models.IntegerField()
    cast_order = models.IntegerField(blank=True, null=True)
    character = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies_cast'


class MoviesDe(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    poster_image_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies_de'


class MoviesSimilar(models.Model):
    movie_id = models.IntegerField()
    similar_id = models.IntegerField()
    correlation = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies_similar'


class NewMoviesFr(models.Model):
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    poster_image_path = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_movies_fr'


class NewMoviesIt(models.Model):
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    poster_image_path = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_movies_it'


class NewMoviesNl(models.Model):
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    poster_image_path = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_movies_nl'


class NewMoviesPl(models.Model):
    title = models.CharField(max_length=255)
    plot = models.TextField(blank=True, null=True)
    poster_image_path = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_movies_pl'


class OldMovieRatings(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'old_movie_ratings'


class OrderRecPool(models.Model):
    score = models.FloatField()
    movie_id = models.IntegerField()
    rec_sender_id = models.IntegerField()
    rec_receiver_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_rec_pool'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class People(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class PersonRole(models.Model):
    person = models.ForeignKey('Persons', models.DO_NOTHING)
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person_role'


class PersonalMovieOrderListing(models.Model):
    movie_id = models.IntegerField()
    user = models.ForeignKey('users.Users', models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'personal_movie_order_listing'


class Persons(models.Model):
    name = models.CharField(max_length=64)
    tmdb_key_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persons'


class QuickSuggestMovies(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'quick_suggest_movies'


class QuicksuggestAction(models.Model):
    command = models.CharField(max_length=255)
    startlist_id = models.IntegerField()
    resultlist_id = models.IntegerField()
    created_at = models.DateTimeField()
    cookie_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quicksuggest_action'


class RecommendationEngine(models.Model):
    type = models.ForeignKey('RecommendationType', models.DO_NOTHING)
    relation_item = models.IntegerField()
    script = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommendation_engine'


class RecommendationEngineTriggers(models.Model):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    trigger = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommendation_engine_triggers'


class RecommendationIgnore(models.Model):
    movie_id = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    engine_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommendation_ignore'


class RecommendationRating(models.Model):
    recommendation_id = models.IntegerField()
    rating_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'recommendation_rating'


class RecommendationRequestResponses(models.Model):
    id = models.AutoField(primary_key=True)
    request_id = models.IntegerField()
    user_id = models.IntegerField()
    list_id = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommendation_request_responses'


class RecommendationRequests(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    list_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommendation_requests'


class RecommendationType(models.Model):
    relation = models.CharField(max_length=127)
    relation_table = models.CharField(max_length=31)

    class Meta:
        managed = False
        db_table = 'recommendation_type'


class Recommendations(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    ranking = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    engine_id = models.IntegerField(blank=True, null=True)
    score_used = models.BooleanField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recommendations'


class RegistrationAccessCodes(models.Model):
    from_user_id = models.IntegerField()
    access_code = models.CharField(max_length=255)
    expired = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'registration_access_codes'


class Roles(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'


class ServiceCinema(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'service_cinema'


class ServiceTv(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'service_tv'


class ServiceTypes(models.Model):
    name = models.CharField(max_length=255)
    shortcut = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_types'


class ServiceUser(models.Model):
    service_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'service_user'


class ServiceVod(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'service_vod'


class Services(models.Model):
    service_type_id = models.IntegerField()
    service_reference_id = models.IntegerField()
    country_id = models.IntegerField()
    icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'services'


class Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    payload = models.TextField()
    last_activity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sessions'


class SimilarityRatings(models.Model):
    user_1_id = models.IntegerField()
    user_2_id = models.IntegerField()
    similar_like = models.IntegerField()
    similar_neutral = models.IntegerField()
    similar_dislike = models.IntegerField()
    size_user_1 = models.IntegerField()
    size_user_2 = models.IntegerField()
    disimilar_like = models.IntegerField()
    disimilar_dislike = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'similarity_ratings'


class TrackerAgents(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    browser = models.CharField(max_length=255)
    browser_version = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name_hash = models.CharField(unique=True, max_length=65, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracker_agents'


class TrackerConnections(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_connections'


class TrackerCookies(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_cookies'


class TrackerDevices(models.Model):
    id = models.BigAutoField(primary_key=True)
    kind = models.CharField(max_length=16)
    model = models.CharField(max_length=64)
    platform = models.CharField(max_length=64)
    platform_version = models.CharField(max_length=16)
    is_mobile = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_devices'
        unique_together = (('kind', 'model', 'platform', 'platform_version'),)


class TrackerDomains(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_domains'


class TrackerErrors(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_errors'


class TrackerEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_events'


class TrackerEventsLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(TrackerEvents, models.DO_NOTHING)
    class_field = models.ForeignKey('TrackerSystemClasses', models.DO_NOTHING, db_column='class_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    log = models.ForeignKey('TrackerLog', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_events_log'


class TrackerGeoip(models.Model):
    id = models.BigAutoField(primary_key=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    country_code3 = models.CharField(max_length=3, blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=2, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    area_code = models.BigIntegerField(blank=True, null=True)
    dma_code = models.FloatField(blank=True, null=True)
    metro_code = models.FloatField(blank=True, null=True)
    continent_code = models.CharField(max_length=2, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_geoip'


class TrackerLanguages(models.Model):
    id = models.BigAutoField(primary_key=True)
    preference = models.CharField(max_length=255)
    language_range = models.CharField(db_column='language-range', max_length=255)  # Field renamed to remove unsuitable characters.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_languages'
        unique_together = (('preference', 'language_range'),)


class TrackerLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey('TrackerSessions', models.DO_NOTHING)
    path = models.ForeignKey('TrackerPaths', models.DO_NOTHING, blank=True, null=True)
    query = models.ForeignKey('TrackerQueries', models.DO_NOTHING, blank=True, null=True)
    method = models.CharField(max_length=10)
    route_path = models.ForeignKey('TrackerRoutePaths', models.DO_NOTHING, blank=True, null=True)
    is_ajax = models.BooleanField()
    is_secure = models.BooleanField()
    is_json = models.BooleanField()
    wants_json = models.BooleanField()
    error = models.ForeignKey(TrackerErrors, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    referer_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracker_log'


class TrackerPaths(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_paths'


class TrackerQueries(models.Model):
    id = models.BigAutoField(primary_key=True)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_queries'


class TrackerQueryArguments(models.Model):
    id = models.BigAutoField(primary_key=True)
    query = models.ForeignKey(TrackerQueries, models.DO_NOTHING)
    argument = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_query_arguments'


class TrackerReferers(models.Model):
    id = models.BigAutoField(primary_key=True)
    domain = models.ForeignKey(TrackerDomains, models.DO_NOTHING)
    url = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    medium = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    search_terms_hash = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracker_referers'


class TrackerReferersSearchTerms(models.Model):
    id = models.BigAutoField(primary_key=True)
    referer = models.ForeignKey(TrackerReferers, models.DO_NOTHING)
    search_term = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_referers_search_terms'


class TrackerRoutePathParameters(models.Model):
    id = models.BigAutoField(primary_key=True)
    route_path = models.ForeignKey('TrackerRoutePaths', models.DO_NOTHING)
    parameter = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_route_path_parameters'


class TrackerRoutePaths(models.Model):
    id = models.BigAutoField(primary_key=True)
    route = models.ForeignKey('TrackerRoutes', models.DO_NOTHING)
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_route_paths'


class TrackerRoutes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_routes'


class TrackerSessions(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    user_id = models.BigIntegerField(blank=True, null=True)
    device = models.ForeignKey(TrackerDevices, models.DO_NOTHING, blank=True, null=True)
    agent = models.ForeignKey(TrackerAgents, models.DO_NOTHING, blank=True, null=True)
    client_ip = models.CharField(max_length=255)
    referer = models.ForeignKey(TrackerReferers, models.DO_NOTHING, blank=True, null=True)
    cookie = models.ForeignKey(TrackerCookies, models.DO_NOTHING, blank=True, null=True)
    geoip = models.ForeignKey(TrackerGeoip, models.DO_NOTHING, blank=True, null=True)
    is_robot = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    language = models.ForeignKey(TrackerLanguages, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracker_sessions'


class TrackerSqlQueries(models.Model):
    id = models.BigAutoField(primary_key=True)
    sha1 = models.CharField(max_length=40)
    statement = models.TextField()
    time = models.FloatField()
    connection_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_sql_queries'


class TrackerSqlQueriesLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    log = models.ForeignKey(TrackerLog, models.DO_NOTHING)
    sql_query = models.ForeignKey(TrackerSqlQueries, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_sql_queries_log'


class TrackerSqlQueryBindings(models.Model):
    id = models.BigAutoField(primary_key=True)
    sha1 = models.CharField(max_length=40)
    serialized = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_sql_query_bindings'


class TrackerSqlQueryBindingsParameters(models.Model):
    id = models.BigAutoField(primary_key=True)
    sql_query_bindings = models.ForeignKey(TrackerSqlQueryBindings, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_sql_query_bindings_parameters'


class TrackerSystemClasses(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tracker_system_classes'


class TriggerPaths(models.Model):
    trigger_path = models.CharField(max_length=255)
    trigger_next_id = models.IntegerField(blank=True, null=True)
    special_check = models.CharField(max_length=15, blank=True, null=True)
    script_to_run = models.CharField(max_length=63, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trigger_paths'


class TriggerPointerUser(models.Model):
    user_id = models.IntegerField()
    trigger_path_id = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trigger_pointer_user'


class TriggerStartingPoints(models.Model):
    path_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=127, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trigger_starting_points'


class Types(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'types'


class UploadImgCollection(models.Model):
    title = models.CharField(max_length=225)
    pub_date = models.DateTimeField()
    updated = models.DateTimeField()
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'upload_img_collection'


class UploadImgCollectionImages(models.Model):
    collection = models.ForeignKey(UploadImgCollection, models.DO_NOTHING)
    image = models.ForeignKey('UploadImgImage', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'upload_img_collection_images'
        unique_together = (('collection', 'image'),)


class UploadImgComment(models.Model):
    text = models.CharField(max_length=225)
    pub_date = models.DateTimeField()
    image = models.ForeignKey('UploadImgImage', models.DO_NOTHING)
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING)
    reply = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upload_img_comment'


class UploadImgImage(models.Model):
    title = models.CharField(max_length=225)
    pub_date = models.DateTimeField()
    col_date = models.DateTimeField()
    image = models.CharField(max_length=100)
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'upload_img_image'


class UploadImgImageLikes(models.Model):
    image = models.ForeignKey(UploadImgImage, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'upload_img_image_likes'
        unique_together = (('image', 'user'),)


class UserRequestRecommendations(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    generated = models.BooleanField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_request_recommendations'






class WatchTogether(models.Model):
    user_1_id = models.IntegerField()
    user_2_id = models.IntegerField()
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'watch_together'


class Watchlists(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)


    # objects = WatchListManager()

    class Meta:
        managed = False
        db_table = 'watchlists'

    @property
    def movies(self):
        
        watch_list = get_object_or_404(Watchlists, id=self.pk)

        movie_ids = MovieWatchlist.objects.values_list('movie_id', flat=True).filter(watchlist_id=self.pk)

        movies = Movies.objects.filter(id__in=movie_ids)
        
        return movies

    @property
    def owner(self):
        
        watch_list = get_object_or_404(Watchlists, id=self.pk)

        user_id = watch_list.user_id
        
        owner = Users.objects.filter(id=user_id)

        return owner

    @property
    def movie_watchlists(self):
        
        watch_list = get_object_or_404(Watchlists, id=self.pk)

        movie_watchlist_ids = MovieWatchlist.objects.values_list('id', flat=True).filter(watchlist_id=self.pk)
        movie_watchlists = MovieWatchlist.objects.filter(id__in=movie_watchlist_ids)
        
        return movie_watchlists


class AWS_link(models.Model):
    small_poster_url = models.CharField(max_length=255, default='https://filmie-storage.s3.eu-central-1.amazonaws.com/movie-posters/w175/')
    medium_poster_url = models.CharField(max_length=255, default='https://filmie-storage.s3.eu-central-1.amazonaws.com/movie-posters/w300/')
    original_poster_url = models.CharField(max_length=255, default='https://filmie-storage.s3.eu-central-1.amazonaws.com/movie-posters/original/')
    list_cover_url = models.CharField(max_length=255, default='https://filmie-storage.s3.eu-central-1.amazonaws.com/list-covers/')
    profile_picture_url = models.CharField(max_length=255, default='https://filmie-storage.s3.eu-central-1.amazonaws.com/profiles/')


class WatchlistTest(models.Model):
    title = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movies)
    user_id = models.ForeignKey('users.Users', on_delete=models.CASCADE)

