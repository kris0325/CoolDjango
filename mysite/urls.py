"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
# from users import views
from users.views import (get_users, get_user, create_user, update_user, delete_user
, export_users_csv, upload_csv_to_db)

urlpatterns = [
    # polls
    # http://localhost:8000/polls/
    path("polls/", include("polls.urls")),
    # http://localhost:8000/adminhabn/
    #     /logic
    # crea/update/query

    path('admin/', admin.site.urls),

    # postgresql
    path('users/getUsers/', get_users, name='get_users'),  # 获取所有用户
    path('users/getUsers/<int:id>/', get_user, name='get_user'),  # 获取单个用户
    path('users/create/', create_user, name='create_user'),  # 创建用户
    path('users/update/<int:id>/', update_user, name='update_user'),  # 更新用户
    path('users/delete/<int:id>/', delete_user, name='delete_user'),  # 删除用户

    # 需求6 下載cvs
    path('users/csv/', export_users_csv, name='export_users_csv'),

    path('users/uploadCsv/', upload_csv_to_db, name='upload_csv_to_db'),

]
