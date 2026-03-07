from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),

    path('advisor/', views.advisor_dashboard, name='advisor_dashboard'),
    path('advisor/approve/<int:pk>/', views.approve_appointment, name='approve_appointment'),
    path('advisor/reject/<int:pk>/', views.reject_appointment, name='reject_appointment'),
]