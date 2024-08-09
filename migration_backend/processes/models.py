from django.db import models


class Rating(models.Model):
    rating = models.IntegerField()
    user = models.IntegerField()
    movie = models.IntegerField()
    timestamp = models.CharField(max_length=100)

    class Meta:
        db_table = "ratings"

    def __str__(self):
        return f"{self.rating} - {self.movie}"
