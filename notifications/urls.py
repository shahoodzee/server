# urls.py
from django.urls import include, path
from rest_framework import routers
from .api import NotificationsViewSet
from . import views

router = routers.DefaultRouter()

router.register(r'notifications', NotificationsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += router.urls