from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, serializers, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitlesFilter
from api.permissions import (AdminOrReadOnlyPermission,
                             AuthorAndStaffOrReadOnlyPermission,
                             IsAdminOrSuperUser)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ProfileSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleCCDSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleCCDSerializer


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnlyPermission, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAndStaffOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.review.all()

    def perform_create(self, serializer):
        try:
            serializer.save(
                author=self.request.user,
                title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
            )
        except IntegrityError:
            raise serializers.ValidationError('Вы уже оставляли отзыв на'
                                              'этот фильм')


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAndStaffOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.filter(review=review, review__title=title)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id')),
        )


@api_view(['post'])
@permission_classes([permissions.AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    email = serializer.data.get('email')
    user, created = User.objects.get_or_create(
        username=username,
        email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    message = (
        f'{username}, ваш код подтверждения: {confirmation_code}'
    )
    send_mail(message=message,
              subject='Подтверждение адреса почты',
              from_email=DEFAULT_FROM_EMAIL,
              recipient_list=[user.email])
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['post'])
@permission_classes([permissions.AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=HTTPStatus.OK
        )
    return Response(
        {'error_message': 'Неверный код или логин пользователя!'},
        status=HTTPStatus.BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=ProfileSerializer
    )
    def profile_me(self, request):
        if request.method == 'PATCH':
            serializer = ProfileSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data,
                status=HTTPStatus.OK
            )
        serializer = ProfileSerializer(self.request.user)
        return Response(serializer.data)
