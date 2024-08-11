from django.contrib import admin

from .models import Rating, Movie, Link, GenomeScore, GenomeTag, Tag, ProcessChunk, UploadedFile

admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(Link)
admin.site.register(GenomeScore)
admin.site.register(GenomeTag)
admin.site.register(Tag)


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'status', "finished_with_errors")


@admin.register(ProcessChunk)
class ProcessChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_file_id', 'start_row', 'end_row', 'status', 'errors')
