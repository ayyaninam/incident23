from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('api/dashboard', dashboard, name="dashboard"),
    path('api/excel_upload', ExportImportExcel.as_view()),
    path('api/handle_upload', handleUpload, name='handleUpload'),
    path('api/signup', signuppage, name='handleUpload'),



    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
