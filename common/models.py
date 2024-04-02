from django.db import models


class CommonModel(models.Model):
    """Common Model Definition"""

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
