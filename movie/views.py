from rest_framework import viewsets

from api.models import Movie, Rating
from movie.serializers import (MovieDetailSerializer, MovieSerializer,
                               RatingSerializer)


class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies viewset."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_serializer_class(self):
        """Retrieve appropriate serializer class."""
        if self.action == 'retrieve':
            return MovieDetailSerializer

        return self.serializer_class


class RatingViewSet(viewsets.ModelViewSet):
    """Manage ratings in database."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
