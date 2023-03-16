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
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        return title.review.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Titles, id=title_id)
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnlyPermission, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        review = get_object_or_404(Review, id=review_id)
        return review.comments.filter(review=review, review__title=title)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=review_id),
            title=get_object_or_404(Titles, id=title_id)
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
