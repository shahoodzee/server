from datetime import datetime, timedelta
from .serializers import ClientSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
    
from django.http import JsonResponse
from user.models import CustomUser, Client, Worker
import jwt

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view




@api_view(['POST'])
def Login(request):
    
    if request.method == 'POST':
        remail = request.data.get('email')
        rpassword = request.data.get('password')
            
        # Query the CustomUser model to find a user with the provided email
        custom_user = CustomUser.objects.filter(email=remail).first()
            
        if custom_user is None:
            return JsonResponse({'message': 'Client not found'})
            
        # Check the password for the CustomUser
        if not custom_user.check_password(rpassword):
            return JsonResponse({"message": "Password is Incorrect"})

        # If the CustomUser exists, check if it has a related Client
        try:
            client = custom_user.client
        except Client.DoesNotExist:
            return JsonResponse({'message': 'Client not found'})
        
        payload = {
            'id' : client.id,                                           # client_id
            'exp': datetime.utcnow() + timedelta(minutes=60),    # expiry date of token
            'iat': datetime.utcnow()                           # token time creation
        }    
        
        token = jwt.encode(payload,'secret', algorithm='HS256')
        
        response = JsonResponse({'jwt': token})
        response.set_cookie(key='jwt', value=token, httponly=True)
        return response

            
api_view(['GET'])
def clientprofile(request):
    if request.method == 'GET':
        token = request.COOKIES.get('jwt')
    
        if not token:
            return JsonResponse( {"message":"Un authenticated"} )
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'] )
        
        except jwt.ExpiredSignatureError:
            return JsonResponse( {"message":"Unauthenticated Session Expired"} )
        
        client = Client.objects.filter(id = payload['id']).first()
        sclient = ClientSerializer(client)
            
    return JsonResponse(sclient.data) 


@csrf_exempt
@api_view(['POST'])
def Logout(request):
    if request.method == 'POST':
        response = JsonResponse({
            'message': 'User Logout Successfully.'
        })
        response.delete_cookie('jwt')
        
        return response


@api_view(['GET'])
def unique_worker_types(request):
    
    if request.method == 'GET':
        # Use distinct to get unique worker types from the database
        unique_types = Worker.objects.values_list('workerType', flat=True).distinct()
        
        # Convert the query result to a list
        unique_types_list = list(unique_types)
        
        # Create a JSON response
        response_data = {'unique_worker_types': unique_types_list}
        
        return JsonResponse(response_data)