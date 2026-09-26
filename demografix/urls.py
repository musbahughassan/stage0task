from django.urls import path
# from .views import GenderizedViewSet
from . import views

urlpatterns = [
    path('classify/', views.gender_list)
]