from rest_framework import serializers
from .models import Link, UploadedFile
from .models import Movie
from .models import Rating
from django.db.models import Avg

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['imdbid', 'tmdbid']

class MovieSerializer(serializers.ModelSerializer):
    link = LinkSerializer(source='link_set.first', read_only=True)
    # average_rating = serializers.SerializerMethodField()
    # num_votes = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['movieid', 'title', 'genres', 'average_rating', 'num_votes', 'link']

    # def get_average_rating(self, obj):
    #     # Calcula a média das avaliações para o filme atual
    #     return obj.rating_set.filter(rating__isnull=False).aggregate(Avg('rating'))['rating_avg'] or 0

    # def get_num_votes(self, obj):
    #     # Conta o número de avaliações para o filme atual
    #     return obj.rating_set.count()
