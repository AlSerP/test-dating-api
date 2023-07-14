from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from time import gmtime, strftime
from django.core.mail import send_mail
from math import sin, cos, acos, pi 


def get_avatar_directory_path(instance, filename):
    upload_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    email_formatted = instance.email.replace('@', '_')
    return f'user_{email_formatted}/{upload_time}/{filename}'


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_male = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to=get_avatar_directory_path, null=True, default=None)

    # Coordinates with an error of +-13 meters
    long = models.DecimalField(max_digits=7, decimal_places=4, default=47.2087)  # Долгота
    lat = models.DecimalField(max_digits=6, decimal_places=4, default=38.9366)  # Широта

    AVATAR_SIZE = (100, 100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def get_distance_to(self, user):
        """
        Calc distance to another user
        """
        def deg_to_rad(x):
            """
            Transform degries to radiance
            """
            return float(x) * pi / 180

        long1 = deg_to_rad(self.long)
        long2 = deg_to_rad(user.long)
        lat1 = deg_to_rad(self.lat)
        lat2 = deg_to_rad(user.lat)

        R = 6371  # Earth radius
        d_long = long1 - long2
        c_angle = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(d_long))

        distance = c_angle * R
        return distance

    def match(self, user):
        """
        Match another user
        """
        print(Match.objects.filter(user_from=self, user_to=user))
        if Match.objects.filter(user_from=self, user_to=user).exists():
            return {'error': 'This user is already matched'}
        
        if Match.objects.filter(user_from=user, user_to=self).exists():
            match = Match.objects.create(user_from=self, user_to=user)
            match.save()
            match.notify()
            return {'message': 'It is mutual match!'}
        
        Match.objects.create(user_from=self, user_to=user)
        return {'message': f'You matched {user}!'}

    @staticmethod
    def get_avatar_size(self):
        return self.AVATAR_SIZE

    def __str__(self):
        return self.email


class Match(models.Model):
    user_from = models.ForeignKey(CustomUser, related_name='match_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUser, related_name='matched_user', on_delete=models.CASCADE)

    def notify(self):
        """
        Send message about match to matched user.
        """
        message = f'Вы понравились {self.user_from.first_name}! Почта участника: {self.user_from}'
        send_mail('Match!', message, "Dating App", [self.user_to], fail_silently=False)
        message = f'Вы понравились {self.user_to.first_name}! Почта участника: {self.user_to}'
        send_mail('Match!', message, "Dating App", [self.user_from], fail_silently=False)
        print('SENDED')
