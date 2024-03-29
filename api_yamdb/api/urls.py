from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, sign_up,
                       token)

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

auth_path = [
    path('auth/signup/', sign_up, name='signup'),
    path('auth/token/', token, name='token'),
]
urlpatterns = [
    path('', include(router.urls)),
    path('', include(auth_path))
]
