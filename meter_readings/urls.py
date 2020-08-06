from django.urls import path
from . import views
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('readings/', views.readings_list, name='readings_list'),
    path('dashboard/readings/new/', views.readings_new, name='readings_new'),
    path('dashboard/users/', views.users_list, name='users_list'),
    path('dashboard/users/<int:pk>/readings', views.user_readings_list, name='user_readings_list'),
    path('dashboard/users/<int:user_id>/readings/<int:pk>/change', views.user_readings_change, name='user_readings_change'),
    path('dashboard/users/<int:user_id>/readings/<int:pk>/remove', views.user_readings_remove, name='user_readings_remove'),
    path('dashboard/statistics', views.statistics, name='statistics'),
    path('dashboard/statistics/hot', views.statistics_hot, name='statistics_hot'),
    path('dashboard/statistics/cold', views.statistics_cold, name='statistics_cold'),
    path('dashboard/admin/new', staff_member_required()(views.AdminRegisterView.as_view()), name='admin_creation'),
    path('dashboard/admin/new/done', views.admin_creation_done, name='admin_creation_done'),
    path('dashboard/profile', views.user_profile, name='user_profile'),
    path('dashboard/profile/edit', views.user_profile_edit, name='user_profile_edit'),
]
