from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from appointments import views

def root_redirect(request):
    return render(request, 'welcome.html')

urlpatterns = [
    path('', root_redirect, name='home'),
    path('admin/', admin.site.urls),

    path('appointments/', include('appointments.urls')),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),

    # ✔ Custom logout (GET allowed)
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='/accounts/login/'),
        name='logout'
    ),

    # ✔ Include Django auth URLs, but WITHOUT overriding logout
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('redirect/', views.role_redirect, name='role_redirect'),
]