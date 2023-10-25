from django.contrib import admin
from entrepreneur.models import EntrepreneurForm, Entrepreneur, EntrepreneurImages

@admin.register(EntrepreneurForm)
class EntrepreneurFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_display_links = ('id', 'title')

@admin.register(Entrepreneur)
class EntrepreneurAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'project_name', 'target_amount', 'amount_collected', 'start_date', 'end_date', 'description', 'is_active', 'income')
    list_display_links = ('id', 'owner')

@admin.register(EntrepreneurImages)
class EntrepreneurImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'entrepreneur')
    list_display_links = ('id', 'entrepreneur')
