from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__' #use all fields
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_manager', 'is_customer']
        extra_kwargs = {
            'password': {'write_only': True}  # don't need to retrieve the password after creation
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # we need to hash the password
        instance = self.Meta.model(**validated_data)  # without the password
        if password is not None:
            instance.set_password(password)  # hash the password
        instance.save()
        return instance
