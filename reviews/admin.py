from django.contrib import admin
from .models import Review


class PosNegFilter(admin.SimpleListFilter):
    title = "Positive / Negative reviews"
    parameter_name = "score"

    def lookups(self, request, model_admin):
        return [("good", "Good"), ("bad", "Bad")]

    def queryset(self, request, reviews):
        eval_word = self.value()
        if not eval_word:
            return reviews
        elif eval_word == "good":
            return reviews.filter(rating__gte=3)
        else:
            return reviews.filter(rating__lt=3)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "experience", "room")
    list_filter = (PosNegFilter, "rating", "user__is_host")
