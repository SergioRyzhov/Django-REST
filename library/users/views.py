import io

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import Serializer, CharField, EmailField
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from .models import Profile


class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class UsersSerializer(Serializer):
    username = CharField(max_length=64)
    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    email = EmailField()

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        instance.save()
        return instance

    def create(self, validated_data):
        user = Profile(**validated_data)
        user.save()
        return user


def get_view(request):
    user = Profile.objects.get(pk=1)
    serializer = UsersSerializer(user)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    print(serializer.data)
    return HttpResponse(json_data)


@csrf_exempt
def post_view(request):
    print(request.body)
    data = JSONParser().parse(io.BytesIO(request.body))

    user = Profile.objects.get(pk=3)

    serializer = UsersSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        print(serializer.validated_data)

        user = serializer.save()
        serializer = UsersSerializer(user)
        render = JSONRenderer()
        json_data = render.render(serializer.data)
        print(serializer.data)
        return HttpResponse(json_data)
