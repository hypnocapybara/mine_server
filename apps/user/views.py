from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from apps.user.serializers import UserSerializer


class CustomAuthTokenView(ObtainAuthToken):
    renderer_classes = (CamelCaseJSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response(UserSerializer(user).data)
