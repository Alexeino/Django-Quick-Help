from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,password,**other_fields):
        if not email:
            raise ValueError("You must provide an email address!")
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name,**other_fields)

        user.set_password(password)
        user.save()

        return user
        

    def create_superuser(self,first_name,last_name,email,password,**other_fields):
        other_fields.setdefault("is_staff",True)
        other_fields.setdefault("is_superuser",True)
        other_fields.setdefault("is_active",True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True") 

        return self.create_user(first_name,last_name,email,password,**other_fields)

# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(max_length=255,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"