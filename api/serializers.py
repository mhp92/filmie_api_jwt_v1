from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
# from rest_framework_jwt.settings import api_settings
from rest_framework.serializers import (
    CharField,
    EmailField,
    ValidationError,
    )


from . models import (
    Movies,
    Watchlists,
    MovieWatchlist,
    WatchlistTest,
    AWS_link,
    Genres,
    GenreMovie,
    Services,
    ServiceVod,
    MovieService,
    )

Users = get_user_model() #this will get any user model that is set in the settings.py file AUTH_USER_MODEL = 'api.Users'

class AWS_linkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AWS_link
        fields = '__all__'

class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = [
                'id',
                'name'
                ]

class MovieSerializer(serializers.ModelSerializer):

    genres = GenresSerializer(many=True, required=False)

    class Meta:
        model = Movies
        fields = [
                'id',
                'title',
                'release_year',
                'poster_image_path',
                'plot',
                'duration',
                'genres',
        ]

class GenreMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenreMovie
        fields = '__all__'


class MovieWatchlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieWatchlist
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = Users
        fields = [
                'id',
                'username',
                'email',
                'email2',
                'verified',
                'password',

        ]
        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    # Validation can/should be done in the custom Users Model
    # in this case validation can be seperate or inside validate_email (see below)
    # def validate(self, data):
    #     email = data['email']
    #     user_qs = Users.objects.filter(email=email)
    #     if user_qs.exists():
    #         raise ValidationError('This Email Adress already exists!')
    #     return data



    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get('email2')
        email2 = value
        if email1 != email2:
            raise ValidationError('Email doesn\'t match!')
        
        user_qs = Users.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError('This Email Address already exists!')

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Email doesn\'t match!')
        return value

    # creating a custom function is in general possible for every Serializer, in the users case is neccessary
    # Use: Validates the password while creating a user inside the api/users/register view 
    # Inside Admin: password is shown as 'algorithm: md5 salt: a2********** hash: e1b5e0**************************' vs 'Invalid password format or unknown hashing algorithm.'
    def create(self, validated_data): 
        print(validated_data)
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = Users(
                username=username,
                email=email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data




class UserLoginSerializer(serializers.ModelSerializer):
    # remember_token = CharField(allow_blank=True, read_only=True)
    token = CharField(allow_blank=True, read_only=True)
    #1beg name or email can be used to login, just remove one of the 2 from below + fields to change behaviour to only one option
    # username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Address', required=False, allow_blank=True)


    class Meta:
        model = Users
        fields = [
                # 'username',
                'id',
                'email',
                'password',
                'token',
        ]
        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    #1end this validation gives the flexibility to either use email OR name, or just email and or just name to login
    def validate(self, data):
        user_obj = None
        email = data.get('email', None) # None is dafault
        username = data.get('username', None)
        password = data['password']
        if not email and not name:
            raise ValidationError('A username or email is required!')
        
        user = Users.objects.filter(
                Q(email=email) |
                Q(username=username)
            ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('Email is not valid!')#('Name or email is not valid!')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Invalid credentials please try again')

        data['token'] = 'PLACE TOKEN HERE'


        return data



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
                'id',
                'username',
                'email',
                'avatar',
                'verified',
                'password',
        ]


# class UserSerializerWithToken(serializers.ModelSerializer):

#     token = serializers.SerializerMethodField()
#     password = serializers.CharField(write_only=True)

#     def get_token(self, obj):
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#         payload = jwt_payload_handler(obj)
#         token = jwt_encode_handler(payload)
#         return token

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance

#     class Meta:
#         model = Users
#         fields = ('token', 'username', 'password')



class WatchlistSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)
    owner = UserSerializer(many=True, required=False)
    # movie_watchlists = MovieWatchlistSerializer(many=True, required=False)
    
    class Meta:
        model = Watchlists
        # fields = '__all__'
        fields = [
                'id',
                'user_id',
                'type_id',
                'title',
                'cover',
                'description',
                'slug', 
                'is_public',
                'owner',
                # 'movie_watchlists',
                'movies',

        ]
        
class WatchlistTestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WatchlistTest
        fields = '__all__'
        depth = 0



class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = '__all__'


class ServiceVodSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceVod
        fields = '__all__'


class MovieServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieService
        fields = '__all__'



