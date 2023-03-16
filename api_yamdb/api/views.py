from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.permissions import AuthorOrReadOnlyPermission
from api.serializers import (CommentSerializer, ReviewSerializer,
                             TitlesSerializer, UserSerializer)
from review.models import Comment, Review, Titles, User


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnlyPermission,)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnlyPermission, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
