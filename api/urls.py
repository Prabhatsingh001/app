from studybudy import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('dashboard/', views.dashboard),
    path('update_profile/', views.Update_Profile),
    path('delete_profile', views.delete_profile),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]