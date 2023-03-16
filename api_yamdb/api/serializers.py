from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import validate_username
from review.models import Titles, Category, Genre

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
                queryset=User.objects.all(),
                error_messages={
                    'unique': ('Логин уже занят!'), },
            ),
            validate_username,
        )
    )
    email = serializers.EmailField(
        required=True,
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                error_messages={
                    'unique': ('Данный email уже зарегестрирван!'),
                }
            ),
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email',)


class ProfileSerializer(
    SignupSerializer,
    UserSerializer
):
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
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Titles
        field = '__all__'

    def get_rating(self, obj):
        return obj.get_rating()
