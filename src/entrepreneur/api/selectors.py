from django.db.models.query import QuerySet
from entrepreneur.models import Entrepreneur, EntrepreneurImages


def entrepreneur_list() -> QuerySet[Entrepreneur]:
    qs = Entrepreneur.objects.select_related('owner').order_by("-project_name").all()
    return qs


def entrepreneur_images_list() -> QuerySet[EntrepreneurImages]:
    qs = EntrepreneurImages.objects.select_related('entrepreneur').order_by("-pk").all()
    return qs
