from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CommentsViewSet, ReviewViewSet, TitleViewSet,
                       UserViewSet, CategoryViewSet, GenreViewSet,)

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


urlpatterns = [
    path('', include(router.urls)),
]
