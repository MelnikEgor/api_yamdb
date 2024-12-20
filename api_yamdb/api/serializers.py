from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)

    def create(self, validated_data):
        print(self.request.data)
        # serializer = UserSerializer(data=request.data)
        if self.request.data['username'] != 'me':
            return User.objects.create(**validated_data)
            # return super().create(request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
