from django.urls import path

from . import views


app_name = 'main'

urlpatterns = [
    path('search/', views.search_results, name='search'),
    path('category/<int:category_id>/', views.ByCategory.as_view(), name='by-category'),
    path('', views.HomePageView.as_view(), name='home-page'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

]