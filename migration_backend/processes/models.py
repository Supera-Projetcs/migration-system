from django.db import models


class Movie(models.Model):
    movieid = models.IntegerField(primary_key=True, unique=True, auto_created=False)
    title = models.CharField(max_length=255, null=True)
    genres = models.CharField(max_length=255, null=True)

class Link(models.Model):
    movieid = models.IntegerField()
    imdbid = models.CharField(max_length=100, null=True)
    tmdbid = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "links"

    def __str__(self):
        return f"{self.movieid} - {self.imdbid} - {self.tmdbid}"

class GenomeScore(models.Model):
    movieid = models.IntegerField(null=True)
    tagid = models.IntegerField(null=True)
    relevance = models.FloatField(null=True)

    class Meta:
        db_table = "genome_scores"

    def __str__(self):
        return f"{self.tagid} - {self.movieid} - {self.relevance}"

class GenomeTag(models.Model):
    tagid = models.IntegerField(null=True)
    tag = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "genome_tags"

    def __str__(self):
        return f"{self.tagid} - {self.tag}"

class Rating(models.Model):
    userid = models.IntegerField(null=True)
    movieid = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    timestamp = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "ratings"

    def __str__(self):
        return f"{self.rating} - {self.movieid}"

class Tag(models.Model):
    userid = models.IntegerField(null=True)
    movieid = models.IntegerField(null=True)
    tag = models.CharField(max_length=255, null=True)
    timestamp = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f"{self.tag} - {self.movieid}"
