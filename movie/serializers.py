from rest_framework import serializers
from api.models import Movie, Rating


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for ratings."""

    class Meta:
        model = Rating
        fields = ('id', 'stars', 'movie', 'user')
        read_only_field = ('id',)


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movies."""

    ratings = serializers.PrimaryKeyRelatedField(
        queryset=Rating.objects.all(),
        many=True,
    )

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'ratings', 'poster')
        read_only_fields = ('id',)


class MovieDetailSerializer(MovieSerializer):
    """Serializer for a movie detail."""

    ratings = RatingSerializer(many=True, read_only=True)
