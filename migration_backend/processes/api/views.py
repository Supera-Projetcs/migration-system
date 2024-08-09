from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from migration_backend.processes.tasks import all_files


class ReadTestView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        all_files.delay()
        return Response({"message": "File reading started"}, status=status.HTTP_200_OK)
