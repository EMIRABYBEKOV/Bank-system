from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string


class AccountManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, email, user_name, last_name, phone, date_of_birth,  password, **extra_fields):
        if not email: raise ValueError('email is required')
        if not user_name: raise ValueError('username is required')
        if not last_name: raise ValueError('last_name is required')
        if not date_of_birth: raise ValueError('date of birth is required')
        if not phone: raise ValueError('phone is required')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          user_name=user_name.capitalize(),
                          last_name=last_name.capitalize(),
                          phone=phone,
                          date_of_birth=date_of_birth,
                          **extra_fields)
        user.set__password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, user_name, last_name, phone,  **extra_fields):
        if not email: raise ValueError('Email is required')
        if not user_name: raise ValueError('username is required')
        if not last_name: raise ValueError('last_name is required')
        if not phone: raise ValueError('phone is required')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          user_name=user_name.capitalize(),
                          last_name=last_name.capitalize(),
                          phone=phone,
                          **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def search(self, query, field):
        if field == 'pk':
            return Account.objects.filter(pk=int(query))
        elif field == 'username':
            return Account.objects.filter(username__icontains=query)
        elif field == 'user_name':
            return Account.objects.filter(user_name__icontains=query)
        elif field == 'last_name':
            return Account.objects.filter(last_name__icontains=query)
        elif field == 'identify_number':
            return Account.objects.filter(identify_number=query)




def get_code():
    code = get_random_string(length=6, allowed_chars='1234567890')
    return code

def get_identify_number():
    code = get_random_string(length=10, allowed_chars='1234567890')
    return code



MALE = 'male'
FEMALE = 'female'
SEX_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)


class Account(AbstractUser):
    # username = None
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    date_of_birth = models.DateField(null=True)
    address = models.TextField(blank=True, null=True)
    phone = PhoneNumberField(unique=True)
    identify_number = models.CharField(max_length=10, default=get_identify_number())
    sex = models.CharField(choices=SEX_CHOICES, max_length=6)
    verification_code = models.CharField(max_length=6, default=get_code)
    verification = models.BooleanField(default=False)
    confidence = models.BooleanField(default=False)
    cards = models.PositiveIntegerField(default=0)


    objects = AccountManager()
    REQUIRED_FIELDS = ['email', 'user_name', 'last_name', 'phone']

    def __str__(self):
        return f"{self.username}"




