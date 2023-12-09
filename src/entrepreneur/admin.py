from django.contrib import admin
from entrepreneur.models import Entrepreneur, EntrepreneurImages

@admin.register(Entrepreneur)
class EntrepreneurAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'owner', 'project_name', 'start_date', 'end_date', 'finished_date', 
        'is_active', 'count', 'purchase_price', 'sale_price', 'total_investment', 
        'gross_income', 'platform_cost', 'final_profit', 'investor_share', 'entrepreneur_share',
        'debt_to_the_fund', 'charity_to_the_fund', 'profit_ratio', 'amount_collected', 'is_finished'
    )
    list_display_links = ('id', 'owner')

@admin.register(EntrepreneurImages)
class EntrepreneurImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'entrepreneur')
    list_display_links = ('id', 'entrepreneur')
