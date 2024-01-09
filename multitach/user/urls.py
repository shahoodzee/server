

# urls.py
from django.urls import include, path
from rest_framework import routers
from .api import WorkerViewSet,ClientViewSet
from notifications.views import create_task_notification,WorkerAcceptTask,WorkerNotificationList,ClientNotificationList,WorkerSeenTask,WorkerRejectTask
from task.views import TaskViewSet, post_a_task, update_a_task, delete_a_task, tasks_list, recommended_workers
from . import views
from feedback.api import FeedbackViewSet
from notifications.api import NotificationsViewSet

router = routers.DefaultRouter()

router.register(r'workers', WorkerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'feedback',FeedbackViewSet)
router.register(r'notifications',NotificationsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/Worker/Types/',views.unique_worker_types),

    #worker and client signup
    path('api/update/client/',views.update_client),    
    path('api/update/worker/',views.update_worker),    
    
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
    path('api/task/recommended_workers/', recommended_workers),
    path('api/task/update_a_task/',update_a_task),
    path('api/task/delete_a_task/',delete_a_task),
    path('api/task/tasks_list/',tasks_list),

    #Task Notifications URLS
    path('api/Client/notifications/createNoti/', create_task_notification),
    path('api/Client/notifications/', ClientNotificationList),
    
    path('api/Worker/notifications/', WorkerNotificationList),
    path('api/Worker/notifications/SeenTask/',WorkerSeenTask),
    path('api/Worker/notifications/taskAccept/', WorkerAcceptTask),
    path('api/Worker/notifications/taskReject/', WorkerRejectTask),   
    
    
    

    
    
]

urlpatterns += router.urls