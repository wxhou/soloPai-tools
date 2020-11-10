from django.urls import path, re_path
from loadtest import views

app_name = 'loadtest'

urlpatterns = [
    path('', views.ProductView.as_view(), name='product'),
    path('index/', views.ProductView.as_view()),
    path('<int:pk>/', views.IndexView.as_view(), name='index'),
    re_path(r'^chart/(?P<name>.*)$', views.chart, name='chart'),
    re_path(r'^shows/(?P<name>.*)$', views.shows, name='shows'),
    path('add_tag/', views.add_tag, name='add_tag')
]
