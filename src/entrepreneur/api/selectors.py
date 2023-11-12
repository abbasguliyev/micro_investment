from django.db.models.query import QuerySet
from entrepreneur.models import EntrepreneurForm, Entrepreneur, EntrepreneurImages

def entrepreneur_form_list() -> QuerySet[EntrepreneurForm]:
    qs = EntrepreneurForm.objects.all()
    return qs

def entrepreneur_list() -> QuerySet[Entrepreneur]:
    qs = Entrepreneur.objects.select_related('owner').order_by("-pk").all()
    return qs

def entrepreneur_images_list() -> QuerySet[EntrepreneurImages]:
    qs = EntrepreneurImages.objects.select_related('entrepreneur').all()
    return qs