from rest_framework import viewsets

from api.models import Movie, Rating
from movie.serializers import MovieSerializer, RatingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies viewset."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """Manage ratings in database."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
