import random
import string
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from .models import CustomUser, Reset
from .serializers import CustomUserSerializer
import jwt
from datetime import datetime, timedelta
from .authentication import *
from django.core.mail import send_mail


# Create your views here.
class RegisterAPIView(APIView):
    def post(self,request):
        print('POST METHOD APIVIEW')
        data = request.data
        # print(data)        
        if data['password'] != data['password_confirm']:
            raise APIException("Passwords do not match! Please check...")

        serializer = CustomUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise APIException('User with these credentials does not exist!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password! Try again')

        
        payload  = {
            'id':user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')
        print("Token ======> ",token)

        res = Response()
        res.set_cookie(key='jwt',value=token,httponly=True)
        res.data ={
            'jwt':token
        }
        return res


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data ={
            "message":"sucess"
        }
        return response

class ForgotAPIView(APIView):

    def post(self,request):
        
        if 'email' not in request.data:
            raise exceptions.NotFound("Email Field Required!")

        email = request.data['email']

        # Delete all previous Reset Link entities
        Reset.objects.filter(email = email).delete()

        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) 
        Reset.objects.create(token = token,email = email)

        url = 'http://127.0.0.1:3000/reset/' + token


        # Sending email with custom token for validation

        send_mail(
            subject="Reset Your Password!",
            message='Click <a href="%s">here</a> to Reset Password '%url,
            from_email='admin@example.com',
            recipient_list=[email]
        )

        return Response({
            'message':'success'
        })

class ResetAPIView(APIView):

    def post(self,request):
        data = request.data

        if 'token' and 'password' and 'password_confirm' not in data:
            raise exceptions.NotFound("Some Keys missing!")

        # print(data)        
        if data['password'] != data['password_confirm']:
            raise APIException("Passwords do not match! Please check...")

        reset = Reset.objects.filter(token = data['token']).first()

        if not reset:
            raise exceptions.APIException("Invalid Token or Link!")
        
        user = CustomUser.objects.filter(email = reset.email).first()

        if not user:
            raise APIException("User not found!")

        user.set_password(data['password'])
        user.save()

        return Response({
            'message':'success'
        })