from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("femail", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        KRW = ("krw", "Korean Won")
        USD = ("usd", "US Dollar")

    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    profile_picture = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=20, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=20, choices=CurrencyChoices.choices)
