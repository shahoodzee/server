

# urls.py
from django.urls import include, path
from rest_framework import routers
from .api import WorkerViewSet,ClientViewSet
from task.views import TaskViewSet, post_a_task
from . import views

router = routers.DefaultRouter()

router.register(r'workers', WorkerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/Worker/Types/',views.unique_worker_types),
    path('api/login/client/',views.Login,name="Login"),
    path('api/profile/client/',views.clientprofile),
    path('api/logout/client/',views.Logout),
    
    #post a task URLS.
    path('api/task/post_a_task/', post_a_task),
    
]

urlpatterns += router.urls