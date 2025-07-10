from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet,user_info
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'register', RegisterViewSet)

urlpatterns = [
    path('auth/',include(router.urls)),
    path('auth/login',TokenObtainPairView.as_view(),name='token_obtain_pair') , 
    path('auth/user',user_info,name='user_info')
]
