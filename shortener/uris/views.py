from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404

from uris.serializers import LinkSerializer
from uris.models import Link


class LinkViewSet(
    CreateModelMixin, 
    GenericViewSet
):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()


class ShortView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(Link, **kwargs)
        return link.target_url
 
