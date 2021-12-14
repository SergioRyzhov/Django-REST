from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import Profile


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        # fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']
        fields = '__all__'
