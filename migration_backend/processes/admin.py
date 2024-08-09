from django.contrib import admin

from .models import Rating, Movie, Link, GenomeScore, GenomeTag, Tag

admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(Link)
admin.site.register(GenomeScore)
admin.site.register(GenomeTag)
admin.site.register(Tag)
