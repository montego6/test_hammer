from rest_framework import serializers
from .models import Profile




class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='phone_number', read_only=True)
    invited_users = serializers.SlugRelatedField(slug_field='phone_number', many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'



