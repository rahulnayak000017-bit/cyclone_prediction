from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PredictionHistory


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'prediction_result',
        'confidence',
        'wind_speed',
        'pressure',
        'temperature',
        'created_at'
    )

    list_filter = ('prediction_result', 'created_at', 'user')
    search_fields = ('user__username',)

    ordering = ('-created_at',)