from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet,user_info,LoginView
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'register', RegisterViewSet)

urlpatterns = [
    path('auth/',include(router.urls)),
    path('auth/login',LoginView.as_view(),name='token_obtain_pair') , 
    path('auth/user',user_info,name='user_info'),
    path('auth/token/refresh',TokenRefreshView.as_view(),name='token_refresh')
]
