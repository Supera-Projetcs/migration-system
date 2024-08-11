from rest_framework import serializers
from .models import UploadedFile
from .models import Movie

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    num_votes = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ['movieid', 'title', 'genres', 'average_rating', 'num_votes']
