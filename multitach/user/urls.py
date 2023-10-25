

# urls.py
from django.urls import include, path
from rest_framework import routers
from .api import WorkerViewSet,ClientViewSet
from task.views import TaskViewSet, post_a_task,update_a_task,delete_a_task
from . import views

router = routers.DefaultRouter()

router.register(r'workers', WorkerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/Worker/Types/',views.unique_worker_types),

    #client login and logout
    path('api/login/client/',views.Login),
    path('api/logout/client/',views.Logout),
    
    #worker login and logout
    path('api/login/worker/',views.Worker_Login),
    path('api/logout/worker/',views.Logout),
    
    
    #client and worker profile
    path('api/profile/worker/',views.WorkerProfile),   
    path('api/profile/client/',views.clientprofile),   
    
    
    # Task URLS.
    path('api/task/post_a_task/', post_a_task),
    path('api/task/update_a_task/',update_a_task),
    path('api/task/delete_a_task/',delete_a_task),
    
    
]

urlpatterns += router.urls