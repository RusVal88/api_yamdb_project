from rest_framework import serializers

from review.models import Titles


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        field = ('rating')

    def get_rating(self, obj):
        return obj.get_rating()
