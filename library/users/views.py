from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from .models import Profile


class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
