from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer,NotesSerializer
# Create your views here.
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
      
 
@api_view(['GET'])   
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        'username':user.username,
        'email':user.email,
    })