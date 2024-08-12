from django.db import models

class Movie(models.Model):
    movieid = models.IntegerField(primary_key=True, unique=True, auto_created=False)
    title = models.CharField(max_length=255, null=True)
    genres = models.CharField(max_length=255, null=True)
    average_rating = models.FloatField(null=True, default=0)
    num_votes = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = "movies"

    def __str__(self):
        return f"{self.movieid} - {self.title} - {self.genres}"

class Link(models.Model):
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column="movieid")
    imdbid = models.CharField(max_length=100, null=True)
    tmdbid = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "links"

    def __str__(self):
        return f"{self.movieid} - {self.imdbid} - {self.tmdbid}"

class GenomeScore(models.Model):
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column="movieid")
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
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column="movieid")
    rating = models.FloatField(null=True)
    timestamp = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "ratings"

    def __str__(self):
        return f"{self.rating} - {self.movieid}"

class Tag(models.Model):
    userid = models.IntegerField(null=True)
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column="movieid")
    tag = models.CharField(max_length=255, null=True)
    timestamp = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f"{self.tag} - {self.movieid}"

#listar arquivos carregados
class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Processing')
    success_count = models.IntegerField(default=0, null=False, blank=True)
    error_count = models.IntegerField(default=0, null=False, blank=True)
    processing_duration = models.DurationField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def finished_with_errors(self):
        return self.processchunk_set.filter(status="failed").count()

class ProcessChunk(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    ended = models.DateTimeField(auto_now_add=True)
    start_row = models.IntegerField(null=True)
    end_row = models.IntegerField(null=True)
    status = models.CharField(max_length=255, null=True)
    errors = models.TextField(null=True)

    def finished_with_errors(self):
        return self.processchunk_set.filter(status="failed").count()
