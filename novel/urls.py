"""myNovelSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path
from novel import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/', views.index),
    path('get_img/<novel_id>/', views.get_img,name='get_img'),
    path('novel_list/', views.novel_list,name='novel_list'),
    path('novel_manager/novel_add/', views.novel_add,name='novel_add'),
    path('novel_manager/', views.novel_manager,name='novel_manager'),
    path('novel_manager/<novel_id>/edit/', views.novel_edit,name='novel_edit'),
    path('novel_manager/<novel_id>/delete/', views.novel_delete,name='novel_delete'),
]
