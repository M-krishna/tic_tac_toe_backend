from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView

from authentication.models import ActivationLink, User
from authentication.serializers import UserSerializer, UserActivationSerializer
from tic_tac_toe.response import api_response
from helpers import generate_activation_token, send_user_mail


# Create your views here.


class CheckAuthentication(APIView):

    @api_response
    def get(self, request):
        return {'success': 1, 'status': status.HTTP_200_OK}


class LoginView(APIView):
    permission_classes = (AllowAny, )

    @api_response
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return {'success': 0, 'error': 'Please provide username or password'}
        else:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    user_object = {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'token': token.key
                    }
                    return {'success': 1, 'data': user_object, 'status': status.HTTP_200_OK}
                else:
                    return {'success': 0, 'error': 'Your account is inactive.'}
            else:
                return {'success': 0, 'error': 'Invalid username/password', 'status': status.HTTP_401_UNAUTHORIZED}


class LogoutView(APIView):

    @api_response
    def post(self, request):
        request.user.auth_token.delete()
        return {'success': 1}


class SignUpView(APIView):
    permission_classes = (AllowAny, )

    @api_response
    def post(self, request):
        data = request.data
        user = User.objects.filter(username=data['email'])
        if user:
            return {'success': 0, 'error': 'user already exist', 'status': status.HTTP_409_CONFLICT}
        user_ser = UserSerializer(data=data)
        if user_ser.is_valid():
            user = user_ser.save()
            data = {
                'activation_code': generate_activation_token(),
                'user': user.id
            }
            # saving activation code to Activation Model through UserActivationSerializer
            user_activation_ser = UserActivationSerializer(data=data)
            if user_activation_ser.is_valid(raise_exception=True):
                token = user_activation_ser.save()

                send_user_mail(
                    template="activation.html",
                    first_name=user.first_name,
                    last_name=user.last_name,
                    subject="Activate Account",
                    activation_url="http://localhost:8000?activate="+token.activation_code,
                    user=user
                )
            return {'success': 1, 'status': status.HTTP_201_CREATED}


class ActivateAccountView(APIView):
    permission_classes = (AllowAny, )

    @api_response
    def post(self, request, activation_token):
        activation_token_from_db = ActivationLink.objects.filter(activation_code=activation_token, is_expired=False).first()
        if activation_token_from_db:
            user = User.objects.filter(pk=activation_token_from_db.user_id, is_active=False).first()
            if user:
                user.is_active = True
                user.save()
                return {'success': 1, 'status': status.HTTP_200_OK}
            else:
                return {'success': 0, 'status': status.HTTP_406_NOT_ACCEPTABLE}
        else:
            return {'success': 0, 'status': status.HTTP_400_BAD_REQUEST}
