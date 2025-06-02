"""
URL configuration for bethel_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pilgrims/', include('pilgrimsapp.urls')),
    path('accounts/', include('accountapp.urls')),
    path('profiles/', include('profileapp.urls')),
    path('truths/', include('truthapp.urls')),
    path('ways/', include('wayapp.urls')),
    path('lives/', include('lifeapp.urls')),
    path('comments/', include('commentapp.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 # + static 부분은 media내 모든 파일들을 경로에서 찾을 수 있도록 설정하는 부분임
