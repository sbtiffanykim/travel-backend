from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    """Photo Description"""

    class PhotoKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    file = models.ImageField()
    description = models.CharField(max_length=150)
    kind = models.CharField(max_length=14, choices=PhotoKindChoices.choices)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, blank=True, null=True, related_name='photos')
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, blank=True, null=True, related_name='photos')

    def __str__(self):
        return f'Photo for {self.room if self.kind=='room' else self.experience}'

class Video(CommonModel):
    """Video Description"""

    file = models.FileField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return f'Video for {self.experience}'
