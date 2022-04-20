from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, permissions, status, response, views
from . import serializers
from .models import Account
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import random
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from .permissions import IsOwnerOrReadOnly
import json
from django.shortcuts import get_object_or_404


class AccountRegistrationView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'head']


class AccountView(generics.RetrieveUpdateDestroyAPIView, generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = serializers.UpdateRetrieveAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly, permissions.IsAdminUser]

class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = serializers.UpdateRetrieveAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly, permissions.IsAdminUser]

class SearchListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = serializers.AccountSerializer
    permissions_classes = [permissions.IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q')
        f = self.request.GET.get('f')
        if q and f is not None:
            if f == 'pk' or f == 'username' or f == 'user_name' or f == 'last_name' or f == 'identify_number':
                result = Account.objects.search(q, f)
                if result.exists():
                    return result
                return Account.objects.none()
            return Account.objects.none()


@api_view(['POST'])
def send_mail_for_verification(request, *args, **kwargs):
    if request.user.is_authenticated:
        send_mail(
            'Verification message',
            'This is verification code:\n'
            f'{request.user.verification_code}',
            'emir.qwerty9@gmail.com',
            [f'{request.user.email}'],
            fail_silently=False,
        )
        return Response({"message": 'Successfully sent'})
    return Response({"message": "Error"}, status=400)


@api_view(['POST'])
def check_code_for_verification(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        code = request.data['code']
        v_code = user.verification_code
        if int(code) == int(v_code):
            user.verification = True
            user.save()
            return Response({"message": 'Successfully'})
        return Response({"message": 'Data error'})
    return Response({"message": "Authentication credentials were not provided"}, status=400)
