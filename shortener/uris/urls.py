from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls import include

from uris.views import LinkViewSet
from uris.views import ShortView 


router = DefaultRouter()

router.register("link", LinkViewSet, basename="link")

urlpatterns = [
    path("short/<str:short_code>", ShortView.as_view(), name="short"),
    path('api/', include((router.urls, 'uris'), namespace='api'))
]

