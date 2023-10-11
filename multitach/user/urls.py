

# urls.py
from django.urls import include, path
from rest_framework import routers
from .api import WorkerViewSet,ClientViewSet
from . import views

router = routers.DefaultRouter()

router.register(r'workers', WorkerViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),
    path('api/clients/register/',views.RegisterCLient,name='RegisterCLient'),
    path('api/clients/',views.GetClients, name='GetCLient'),
]

urlpatterns += router.urls