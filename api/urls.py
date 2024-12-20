from studybudy import views
from UploadNotesOrQuestionPaper.views import create_note
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('signup/', views.signup),
    path('dashboard/', views.dashboard),
    path('update_profile/', views.Update_Profile),
    path('delete_profile', views.delete_profile),
    
    path('upload_notes/', create_note),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]