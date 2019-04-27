from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


class UserViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def current(self, request):
        return Response(self.get_serializer(request.user).data)
