from django.contrib import admin

from .models import Rating, Movie, Link, GenomeScore, GenomeTag, Tag, Process, ProcessChunk

admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(Link)
admin.site.register(GenomeScore)
admin.site.register(GenomeTag)
admin.site.register(Tag)


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_of_chunks', 'started', 'finished_chunks', 'finished_with_errors')

@admin.register(ProcessChunk)
class ProcessChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'process_id', 'start_row', 'end_row', 'status', 'errors')
