from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Movie, Rating
from movie.serializers import (MovieDetailSerializer, MovieImageSerializer,
                               MovieRatingSerializer, MovieSerializer,
                               RatingSerializer)


class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies viewset."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )

    def get_serializer_class(self):
        """Retrieve appropriate serializer class."""
        if self.action == 'retrieve':
            return MovieDetailSerializer
        elif self.action == 'upload_image':
            return MovieImageSerializer
        elif self.action == 'rate_movie':
            return MovieRatingSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload cover for a movie."""
        movie = self.get_object()
        serializer = self.get_serializer(
            movie,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=['POST'], detail=True, url_path='rate-movie')
    def rate_movie(self, request, pk=None):
        """Rate a movie."""
        movie = self.get_object()
        user = request.user
        rating = Rating.objects.get(movie=movie.id, user=user.id)

        serializer = self.get_serializer(
            rating,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class RatingViewSet(viewsets.ModelViewSet):
    """Manage ratings in database."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
