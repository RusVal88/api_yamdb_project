from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CommentsViewSet, ReviewViewSet, TitleViewSet,
                       CategoryViewSet, GenreViewSet, UserViewSet,
                       token, sign_up,)

app_name = 'api'

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comment'
)
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', sign_up, name='signup'),
    path('auth/token/', token, name='token'),
]
