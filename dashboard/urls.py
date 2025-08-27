from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('disbursal/', views.dashboard_view, name='disbursal'),  # Disbursal page route
    path('test/', views.test_view, name='test'),  # Test route
    path('authenticate/', views.authenticate_user, name='authenticate'),
    path('logout/', views.logout_view, name='logout'),
    path('api/summary/', views.summary_data, name='summary_data'),
    path('api/charts/', views.charts_data, name='charts_data'),
    path('api/table/', views.table_data, name='table_data'),
    path('api/date-range/', views.date_range, name='date_range'),
    path('api/distinct-values/', views.distinct_values, name='distinct_values'),
]
