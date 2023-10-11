from .serializers import ClientSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
    
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from user.models import Client



@api_view(['GET'])
def GetClients(request):
    if request.method == 'GET':
        workers = Client.objects.all()
        serializer = ClientSerializer(workers, many=True)
        
        #Decrypt the password (if needed)
        password = serializer.data.get('password')  
        #Check if the password field contains a hashed password
        if not password.startswith(('pbkdf2_sha256$', 'bcrypt', 'argon2')):
            # If it doesn't start with a recognized hash identifier, assume it's plain text
            # You may want to handle this differently based on your requirements
            password = make_password(password)
            serializer.data['password'] = password
        
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def RegisterCLient(request):
        if request.method == 'POST':
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(serializer,data=request.data)
                return JsonResponse(serializer.data)    
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
            
