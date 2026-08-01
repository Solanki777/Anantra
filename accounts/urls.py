from django.urls import path
from . import views
from accounts.views import reset_admin_password
from accounts.views import list_users
from .views import create_admin

urlpatterns = [
    
    path("",views.login_view,name="login") ,
    path("register/", views.register_view , name="register"),
    path("logout/" , views.logout_view, name="logout"), 
    path(
    "create-admin/",
    create_admin,
    name="create_admin",
),
   
]

