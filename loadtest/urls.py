from django.urls import path, re_path
from loadtest import views

urlpatterns = [
    path('user/', views.UserView.as_view()),
    path('product/', views.ProductView.as_view())
]
