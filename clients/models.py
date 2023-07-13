from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from time import gmtime, strftime
from django.core.mail import send_mail


def get_avatar_directory_path(instance, filename):
    upload_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    email_formatted = instance.email.replace('@', '_')
    return f'user_{email_formatted}/{upload_time}/{filename}'


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_male = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to=get_avatar_directory_path, null=True, default=None)

    AVATAR_SIZE = (100, 100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    @staticmethod
    def get_avatar_size(self):
        return self.AVATAR_SIZE

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
