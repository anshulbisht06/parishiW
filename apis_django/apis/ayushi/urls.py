from django.urls import path, include
from ayushi import views

urlpatterns = [
	path('error/<int:code>/', views.ErrorPageView.as_view(), name='error_page'),
    path('', views.HomePageView.as_view(), name='home_page'),
    path('<str:category>/item/<str:item_id>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<str:category>/items/<int:page>/', views.ItemsListView.as_view(), name='items_list')
]
