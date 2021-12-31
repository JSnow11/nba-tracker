"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


from frontend import views as feViews
from tracker import views as apiViews

router = routers.DefaultRouter()
router.register(r'teams', apiViews.TeamViewSet, 'teams')
router.register(r'players', apiViews.PlayerViewSet, 'players')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/populate', apiViews.PopulateDB.as_view()),
    path('api/index', apiViews.IndexItems.as_view()),
    path('api/', include(router.urls)),
    path('auth/',
         include('rest_framework.urls', namespace='rest_framework')),

    url('', feViews.index)
]
