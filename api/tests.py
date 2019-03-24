from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from . models import Watchlists, MovieWatchlist, Movies


# can be automated
# new / blank db --> we have to create some test data here



class WatchlistAPITestCase(APITestCase):
    def setUp(self):
        u = User.objects.create_user(username='testuser', email='test@test.com', password='password')
        
        m = Movies.objects.create(
            title='Interstellar',
            plot='someplot',
            release_year='2014',
            poster_image_path='interstellar.jpg'
            )

        wl = Watchlists.objects.create(
            user_id=u.id,
            type_id=1,
            title='APITestcase Watchlist'
            )

        mwl = MovieWatchlist.objects.create(
            movie_id=m.id,
            watchlist_id=wl.id
            )

        def test_single_user(self):
            user_count = User.objects.count()
            self.assertEqual(user_count, 1)
