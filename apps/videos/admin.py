from django.contrib import admin
from .models import Video, VideoProgress
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class VideoResource(resources.ModelResource):
    """
    Resource configuration for the Video model.
    Allows import/export functionality for video data.
    """
    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    """
    Admin configuration for Video model.
    Includes import/export functionality.
    """
    resource_class = VideoResource

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for VideoProgress model.
    Provides filtering, searching, and ordering options.
    """
    list_display = ('user', 'video', 'started', 'last_position', 'completed', 'updated_at')
    list_filter = ('completed', 'started')
    search_fields = ('user__email', 'video__title')
    ordering = ('-updated_at',)
