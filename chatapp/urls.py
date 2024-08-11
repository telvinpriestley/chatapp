from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.home, name='home'),
    path('room_page/<int:room_id>/', views.room_page, name='room_page'),
    
    
    path('signup_view', views.signup_view, name='signup_view'),
    path('login_view', views.login_view, name='login_view'),
   
    path('loginFirst', views.loginFirst, name='loginFirst'),
    path('logout_view/', views.logout_view, name='logout_view'),
    
    path('emailVerification_sign_up', views.emailVerification_sign_up, name='emailVerification_sign_up'),
    path('verification_view', views.verification_view, name='verification_view'),
    path('verification_proper', views.verification_proper, name='verification_proper'),
    
    path('login_email_verify', views.login_email_verify, name='login_email_verify'),
    path('login_verify_view', views.login_verify_view, name='login_verify_view'),
    path('login_proper', views.login_proper, name='login_proper'),
    
    path('add_comment', views.add_comment, name='add_comment'),
    path('add_like/<int:room_id>/', views.add_like, name='add_like'),
    path('add_share/<int:room_id>/', views.add_share, name='add_share'),
    path('add_comment_reply', views.add_comment_reply, name='add_comment_reply'),
    path('add_comment_like/<int:comment_id>/', views.add_comment_like, name='add_comment_like'),
    
    path('room_page/<int:room_id>/', views.room_page, name='room_page'),
    
    path('userinfo/<int:user_id>/', views.userinfo, name='userinfo'),
    path('profile', views.profile, name='profile'),
]