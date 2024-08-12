from rest_framework import serializers
from .models import Link, UploadedFile
from .models import Movie

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

    class Meta:
        model = Movie
        fields = ['movieid', 'title', 'genres', 'average_rating', 'num_votes', 'link']
