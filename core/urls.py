"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from onboarding import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('onboarding/login/<str:token>/', views.login_view, name='login_view'),
    path('onboarding/form/<str:token>/', views.onboarding_form, name='onboarding_form'),
    path('logout/<str:token>/', views.logout_view, name='logout_view'),
    path('change-password/<str:token>/', views.change_password, name='change_password'),

    path('onboarding/personal/<str:token>/', views.personal_view, name='personal_view'),
    path('onboarding/education/<str:token>/', views.education_view, name='education_view'),
    path('onboarding/work/<str:token>/', views.work_view, name='work_view'),
    path('onboarding/documents/<str:token>/', views.document_view, name='document_view'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)