from django.db import models


class Movie(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, auto_created=False)
    title = models.CharField(max_length=255, null=True)
    genres = models.CharField(max_length=255, null=True)

class Link(models.Model):
    movieId = models.IntegerField()
    imdbId = models.CharField(max_length=100, null=True)
    tmdbId = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "links"

    def __str__(self):
        return f"{self.movie} - {self.imdbId} - {self.tmdbId}"

class GenomeScore(models.Model):
    tagId = models.IntegerField(null=True)
    movieId = models.IntegerField(null=True)
    relevance = models.FloatField(null=True)

    class Meta:
        db_table = "genome_scores"

    def __str__(self):
        return f"{self.tagId} - {self.movieId} - {self.relevance}"

class GenomeTag(models.Model):
    tagId = models.IntegerField(null=True)
    tag = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "genome_tags"

    def __str__(self):
        return f"{self.tagId} - {self.tag}"

class Rating(models.Model):
    rating = models.IntegerField(null=True)
    userId = models.IntegerField(null=True)
    movieId = models.IntegerField(null=True)
    timestamp = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "ratings"

    def __str__(self):
        return f"{self.rating} - {self.movie}"

class Tag(models.Model):
    tag = models.CharField(max_length=255, null=True)
    userId = models.IntegerField(null=True)
    movieId = models.IntegerField(null=True)
    timestamp = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f"{self.tag} - {self.movie}"
