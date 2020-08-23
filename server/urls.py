"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from course import views as course_views
from api import  views as api_views
from django.urls import path


urlpatterns = [
    path('temp/',course_views.test_course),
    path('course_info/',api_views.course_info),
    path('comment_info/',api_views.comment_info),
    path('submit_comment/',api_views.submit_comment),
]
