from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from migration_backend.processes.api.views import ReadTestView
from migration_backend.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("read-test/", ReadTestView.as_view(), name="read-test"),
]
urlpatterns += router.urls
