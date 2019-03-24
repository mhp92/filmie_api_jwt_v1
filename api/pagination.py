from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )



class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 20



class MovieLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100



class MoviePageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'