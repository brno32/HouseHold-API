from django.urls import path
from .views import ItemList, ItemDetail, GroupList

urlpatterns = [
    path('', ItemList.as_view()),
    path('<int:pk>/', ItemDetail.as_view()),
    path('groups/', GroupList.as_view())
]
