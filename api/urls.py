from studybudy import views
from studybudy.views import PasswordResetRequestView, PasswordResetConfirmView
from UploadNotesOrQuestionPaper.views import create_note
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),

    path('change_password/', views.change_password),
    # path('forgot_password/', views.reset_password),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    path('dashboard/', views.dashboard),
    path('update_profile/', views.Update_Profile),
    path('delete_profile', views.delete_profile),
    
    path('upload_notes/', create_note),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]