from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from migration_backend.processes.api.views import ReadTestView
from migration_backend.users.api.views import UserViewSet
from migration_backend.processes.views import UploadFilesView, ListUploadedFilesView, MovieSearchView, GenreListView

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("read-test/", ReadTestView.as_view(), name="read-test"),
    path('upload/', UploadFilesView.as_view(), name='upload-files'),
    path('uploaded-files/', ListUploadedFilesView.as_view(), name='list-uploaded-files'),
    path('movies/search/', MovieSearchView.as_view(), name='movie-search'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
]
urlpatterns += router.urls
