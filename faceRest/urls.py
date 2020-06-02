"""faceRest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Local view apps
from core import views as core_views
from faceRest import settings
from persons import views as persons_views
from faces import views as faces_views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from django.conf.urls.static import static
from system.views import train_info_view, train_view

router = routers.DefaultRouter()
router.register(r'persons', persons_views.PersonViewSet, basename='Persons')
router.register(r'labels', persons_views.LabelViewSet, basename='Labels')
router.register(r'detfaces', faces_views.FaceDetectedViewSet, basename='detfaces')
router.register(r'dataset', faces_views.FaceDataSetViewSet, basename='dataset')
# router.register('person/<int:pk>', persons_views.PersonDetail)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('system/train_info', train_info_view, name='train_info'),
    path('system/train', train_view, name='train'),
    path('personsl/', persons_views.persons_list),
    path('person/<int:pk>/', persons_views.PersonDetail.as_view()),
    path('hello/', core_views.HelloView.as_view(), name='hello'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
