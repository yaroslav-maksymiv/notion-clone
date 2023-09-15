from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import Token

from .models import CustomUser
from .serializers import UserSerializerWithToken, UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def check_token_valid(request):
    try:
        token = request.POST.get('token')
        jwt_token = Token(token)
        is_valid = jwt_token.is_valid()
        if is_valid:
            return Response(status=status.HTTP_200_OK)  
        return Response(status=status.HTTP_401_UNAUTHORIZED)    
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)    


class CustomUserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Received Headers:", request.headers)
        data = request.data
        try:    
            user = CustomUser.objects.create(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=make_password(data['password'])
            )
            serializer = UserSerializerWithToken(user)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status.HTTP_400_BAD_REQUEST)

        
# JWT Token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
       
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
            
        data.pop('refresh')
        data.pop('access')
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer        
    
    
    