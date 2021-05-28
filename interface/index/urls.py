from django.urls import path

from index import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('refactoring/<int:refactoring_id>/', views.refactoring_detail, name='refactoring_detail')
]
