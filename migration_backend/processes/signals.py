from django.db.models.signals import post_save
from django.dispatch import receiver
from migration_backend.processes.models import Rating
from django.db.models import Avg

@receiver(post_save, sender=Rating)
def update_movie_ratings(sender, instance, **kwargs):
    # acessa o id do filme na avaliacao
    if instance.movieid:
        movie = instance.movieid
        average_rating = Rating.objects.filter(movieid=movie).aggregate(Avg('rating'))['rating__avg']
        num_votes = Rating.objects.filter(movieid=movie).count()

        # atualiza o modelo de movie
        movie.average_rating = average_rating or 0
        movie.num_votes = num_votes
        movie.save()
