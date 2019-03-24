from django.urls import path, include
from django.contrib import admin 
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token




# from .view import UserCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_jwt_token), #06.03 added /auth/
    path('api/token/refresh/', refresh_jwt_token),
    path('api/token/verify/', verify_jwt_token),
    path('api/users/', include('api.urls', namespace='users-api')),
    path('router/', include('api.router_urls')),
    path('api/', include('api.auth_urls', namespace="auth"))
]


