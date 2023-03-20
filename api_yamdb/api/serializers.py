from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .validators import validate_username
from review.models import Category, Genre, Titles, Review, Comment


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'role',
            'email',
            'bio',
        )


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=(
            UnicodeUsernameValidator(
                regex=r'^[a-zA-Z0-9_-]+$'), ),
        error_messages={'unique': ('Логин уже занят!'), },
    )
    email = serializers.EmailField(
        required=True,
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),),),
        error_messages={
            'unique': ('Данный email уже зарегестрирван!'),
        }
    )
        

    class Meta:
        model = User
        fields = ('username', 'email',)

    class Meta:
        model = User
        fields = ('username', 'email',)

    class Meta:
        model = User
        fields = ('username', 'email',)


class ProfileSerializer(SignupSerializer, UserSerializer):
    role = serializers.CharField(read_only=True)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=50,
    )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Titles
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category',)

    def get_rating(self, obj):
        reviews = obj.review.all()
        if reviews:
            avg_scores = (
                (sum(review.score for review in reviews))
                / len(reviews)
            )
            return round(avg_scores, 0)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'titles')
            )
        ]

    def validate(self, data):
        if data.get('score') not in data.get('score_value'):
            raise serializers.ValidationError(
                'Переданное значение "score" недопустимо.'
                'Укажите число от 1 до 10.'
            )
        if not data.get('score'):
            raise serializers.ValidationError('Задайте значение "score".')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        field = '__all__'
        read_only_field = ('review')
