from django.urls import path 
from . import views



urlpatterns = [
    path('',views.dashboard_page,name='dashboard'),
    path('login/',views.login_user,name='login'),
    path('otp/', views.otp_view, name='otp'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),

    path('add_poll_stations/',views.add_poll_stations, name='add_poll_stations'),
    path('poll_stations/', views.poll_station, name='poll_station'),
    path('poll_station_view/<int:station_id>', views.poll_station_view, name='poll'),
    path('poll_station_view/<int:station_id>/register-poll-agent', views.register_poll_agent, name='reg_poll_agent'),
    path('poll_station_view/<int:station_id>/presidential-form', views.add_pres_result, name='pres_result'),
    path('poll_station/<int:station_id>/parliamentary-form', views.add_parl_result, name='parl_result'),
    path('update_pollstation/<int:station_id>', views.update_pollstation, name='updatePollstation'),
    path('delete_pollstation/<int:station_id>', views.delete_pollstation, name='delete'),

    path('update_presidential_results/<int:station_id>/<int:pres_id>', views.update_presidential, name='updatePres'),
    path('delete_presidential_results/<int:station_id>/<int:pres_id>', views.delete_presidential, name='delete_pres'),
    path('update_parliamentary_results/<int:station_id>/<int:parl_id>', views.update_parliamentary, name='updateParl'),
    path('delete_parliamentary_results/<int:station_id>/<int:parl_id>', views.delete_parliamentary, name='delete_parl'),

]