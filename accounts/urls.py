from django.urls import path
from . import views
from .views import create_admin,test_smtp

urlpatterns = [
    
    path("",views.login_view,name="login") ,
    path("register/", views.register_view , name="register"),
    path("logout/" , views.logout_view, name="logout"), 
    path(
    "create-admin/",
    create_admin,
    name="create_admin",
),
path("test-smtp/", test_smtp),
]

