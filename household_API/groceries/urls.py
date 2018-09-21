from django.urls import path
from .views import ItemList, ItemDetail, GroupList, GroupDetail

urlpatterns = [
    path('', ItemList.as_view()),
    path('<int:pk>/', ItemDetail.as_view()),
    path('groups/', GroupList.as_view()),
    path('groups/<int:pk>/', GroupDetail.as_view()),
]
