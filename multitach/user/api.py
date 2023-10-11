from rest_framework import viewsets
from .serializers import WorkerSerializer, ClientSerializer
# views.py
from .models import CustomUser, Worker, Client

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    