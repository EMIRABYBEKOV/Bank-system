from rest_framework import serializers
from .models import Account
from rest_framework.exceptions import ValidationError


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    c_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = (
            'identify_number',
            'username',
            'user_name',
            'last_name',
            'confidence',
            'date_of_birth',
            'email',
            'phone',
            'sex',
            'address',
            'password',
            'c_password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'identify_number': {'read_only': True},
            'confidence': {'read_only': True},
        }

    def validate(self, validated_data):
        if validated_data['c_password'] == validated_data['password']:
            validated_data.pop('c_password')
            return validated_data
        raise ValidationError('Passwords have to be same')

    def save(self, **kwargs):
        account = Account(username=self.validated_data['username'],
                          user_name=self.validated_data['user_name'],
                          last_name=self.validated_data['last_name'],
                          date_of_birth=self.validated_data['date_of_birth'],
                          email=self.validated_data['email'],
                          phone=self.validated_data['phone'],
                          sex=self.validated_data['sex'],
                          address=self.validated_data['address'],
                          confidence=self.validated_data['confidence']
                          )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()





class UpdateRetrieveAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'pk',
            'identify_number',
            'username',
            'user_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone',
            'sex',
            'confidence',
        )
        extra_kwargs = {
            'pk': {'read_only': True},
            'identify_number': {'read_only': True},
        }


