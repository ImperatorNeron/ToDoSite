from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.text import slugify


class CustomUser(AbstractUser):
    """User class extension"""

    # Validator for number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='False number. Example: +380000000000')
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    score = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    # ToDo: UserIcon should be in settings like 'settings.USER_ICON_ROOT'
    photo = models.ImageField(upload_to='UserIcon/%Y/%m/%d', blank=True)
    slug = models.SlugField(blank=True)

    # Do slag
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Task(models.Model):
    """ Task model """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    # ToDo: typo "creation_date"
    creation_data = models.DateTimeField(auto_now_add=True)
    to_do_date = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'

    # For admin panel
    # ToDo: if you use localization use it everywhere, like everything in english, or in ukrainian
    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'
        ordering = ['to_do_date', 'title']


class SiteImages(models.Model):
    """ Model for site images """
    caption = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='SitePhotos')
