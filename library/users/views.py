import io

from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer, CharField, EmailField, ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class UsersSerializer(Serializer):
    username = CharField(max_length=64)
    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    email = EmailField()

    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError('Name must be more then 3 ch length')
        return value

    def validate(self, attrs):
        if attrs.get('first_name') == 'ololo' and attrs['username'] != 'xxx':
            raise ValidationError('username must be xxx')
        return attrs

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

    if request.method == 'POST':
        serializer = UsersSerializer(data=data)
    elif request.method == 'PUT':
        user = Profile.objects.get(pk=3)
        serializer = UsersSerializer(user, data=data)
    elif request.method == 'PATCH':
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
    else:
        return HttpResponseServerError(serializer.errors.get('non_field_errors'))
