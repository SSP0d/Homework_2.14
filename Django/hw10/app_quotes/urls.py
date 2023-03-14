from . import views
from django.urls import path

app_name = 'app_quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:id>/', views.about_author, name='about_author'),
    path('add_author', views.add_author, name="add_author"),
    path('add_quote', views.add_quote, name="add_quote")
]
