from rest_framework.serializers import ModelSerializer
from .models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = Profile
        # fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']
        fields = '__all__'
