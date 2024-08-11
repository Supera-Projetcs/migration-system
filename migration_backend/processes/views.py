from config import settings
from migration_backend.processes.tasks import stream_csv_in_chunks
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import os

from rest_framework.generics import ListAPIView
from .models import Movie, UploadedFile
from .serializers import MovieSerializer, UploadedFileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Avg, Count
from django.db.models import Func, CharField, Q

class UploadFilesView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        upload_info = []

        for file in files:
            file_path = os.path.join(settings.BASE_DIR, 'files', file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # create an uploadedFile record
            uploaded_file = UploadedFile.objects.create(
                file_name=file.name,
                status='Processing',
                start_time=timezone.now()  # tempo de inicio
            )

            stream_csv_in_chunks.delay(file_path, uploaded_file.id)

            upload_info.append({
                'file_name': file.name,
                'start_time': uploaded_file.start_time,
                'status': 'Processing started',
            })

        return Response(upload_info, status=status.HTTP_201_CREATED)

class UploadedFileListView(ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer


class ExtractYearFromTitle(Func):
    function = 'regexp_matches'
    template = "%(function)s(%(expressions)s, '\\((\\d{4})\\)', 'g')[1]" # extrair 4 digitos dentro de parenteses (ano)

    def __init__(self, expression, **extra):
        super().__init__(expression, output_field=CharField(), **extra)
class MovieSearchView(ListAPIView):
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genres']
    search_fields = ['title']

    def get_queryset(self):
        queryset = Movie.objects.annotate(
            average_rating=Avg('rating__rating'), # media de avaliacoes
            num_votes=Count('rating') # numero de avaliacoes
        )

        min_rating = self.request.query_params.get('min_rating')
        min_votes = self.request.query_params.get('min_votes')
        user_id = self.request.query_params.get('user_id')
        year_start = self.request.query_params.get('year_start')
        year_end = self.request.query_params.get('year_end')
        genres = self.request.query_params.get('genres')

        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        if min_votes:
            queryset = queryset.filter(num_votes__gte=min_votes)
        if user_id:
            queryset = queryset.filter(rating__userId=user_id)
        if year_start and year_end:
            queryset = queryset.filter(release_year__range=[year_start, year_end])
        if genres:
            # filtra pelos gêneros fornecidos, divididos por vírgula ou pipe
            genre_list = genres.split('|')
            query = Q()
            for genre in genre_list:
                query |= Q(genres__icontains=genre)
            queryset = queryset.filter(query)

        return queryset


class GenreListView(APIView):
    def get(self, request):
        genres = Movie.objects.values_list('genres', flat=True).distinct()
        genre_list = set()
        for genre_str in genres:
            genre_list.update(genre_str.split('|'))
        return Response(sorted(genre_list))
