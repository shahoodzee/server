# urls.py
from django.urls import include, path
from rest_framework import routers
from .api import FeedbackViewSet

router = routers.DefaultRouter()

router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += router.urls