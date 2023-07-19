from django.urls import path
from .views import *

urlpatterns = [
    path('', loginAdmin.as_view()),
    path('system/', check.as_view()),
    path('check_controller', check_controller),
    path('logout/', Logout.as_view()),
    path('subequip/', getSubEquipment.as_view()),
    path('search/', searchFilter.as_view()),
    path('edit-system/<id>', EditSystem.as_view()),
    path('delete-system/<id>', deleteSystem.as_view()),
]