from django.conf import settings
from django.dispatch import receiver
from migration_backend.processes.filters import MovieFilter
from migration_backend.processes.tasks import stream_csv_in_chunks
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import os
from django.db.models import Q, Count


from rest_framework.generics import ListAPIView
from .models import Movie, UploadedFile
from .serializers import MovieSerializer, UploadedFileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Avg
from django.db.models import Func, CharField
from rest_framework.permissions import AllowAny


class UploadFilesView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    authentication_classes = []

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
                'id': uploaded_file.id,
                'file_name': uploaded_file.file_name,
                'uploaded_at': uploaded_file.start_time,
                'status': uploaded_file.status,
                'success_count': uploaded_file.success_count,
                'error_count': uploaded_file.error_count,
                'processing_duration': uploaded_file.processing_duration,
                'start_time': uploaded_file.start_time,
                'end_time': uploaded_file.end_time
            })

        return Response(upload_info, status=status.HTTP_201_CREATED)

class UploadedFileListView(ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class ExtractYearFromTitle(Func):
    function = 'regexp_replace'
    template = "%(function)s(%(expressions)s, '\\D*(\\d{4})\\D*', '\\1', 'g')"
    output_field = CharField()

    def __init__(self, expression, **extra):
        super().__init__(expression, output_field=CharField(), **extra)

class MovieSearchView(ListAPIView):
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MovieFilter
    search_fields = ['title']
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):

        min_rating = self.request.query_params.get('min_rating')
        min_votes = self.request.query_params.get('min_votes')
        user_id = self.request.query_params.get('user_id')
        year_start = self.request.query_params.get('year_start')
        year_end = self.request.query_params.get('year_end')

        query = Q()

        if min_rating:
            query &= Q(rating__rating__gte=min_rating)
        if min_votes:
            query &= Q(rating__count__gte=min_votes)
        if user_id:
            query &= Q(rating__user_id=user_id)
        if year_start and year_end:
            query &= Q(release_year__gte=year_start) & Q(release_year__lte=year_end)
        elif year_start:
            query &= Q(release_year__gte=year_start)
        elif year_end:
            query &= Q(release_year__lte=year_end)

        queryset = Movie.objects.annotate(
            release_year=ExtractYearFromTitle('title')  # Extraindo o ano do título
        ).filter(query)

        queryset = queryset.distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class GenreListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):
        genres = Movie.objects.values_list('genres', flat=True).distinct()
        genre_list = set()
        for genre_str in genres:
            genre_list.update(genre_str.split('|'))
        return Response(sorted(genre_list))


class ListUploadedFilesView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):
        uploaded_files = UploadedFile.objects.all()
        serializer = UploadedFileSerializer(uploaded_files, many=True)
        return Response(serializer.data)
