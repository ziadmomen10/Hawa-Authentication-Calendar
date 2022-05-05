from django.core import exceptions
from rest_framework import serializers
from .models import Period, User
import django.contrib.auth.password_validation as validators

class RegisterSerilaziers(serializers.ModelSerializer):
    """
    custom register serilizer for custom user Model

    """
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name",
                  "last_name", "phone_number", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        get validated_data make validation in password create user
        or return error list

        """
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        errors = dict()
        try:
            if password is not None:
                validators.validate_password(password=password, user=instance)
                instance.set_password(password)
                instance.save()
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return instance


class PeriodDateSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 1
        model = Period
        fields = '__all__'
    

    def create(self, validated_data):
        return Period.objects.create(user=self.context.get('request').user, **validated_data)




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"