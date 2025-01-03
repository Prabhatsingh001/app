from studybudy import views
from UploadNotesOrQuestionPaper.views import create_note, create_question_paper, view_notes, get_question_paper
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # signup login and logout
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('delete_profile_picture/', views.delete_profile_picture),

    # forgot password and change password
    path('change_password/', views.change_password),

    # dashboard and profile
    path('dashboard/', views.dashboard),
    path('update_profile/', views.Update_Profile),
    path('delete_profile', views.delete_profile),
    
    # upload notes and question paper
    path('upload_notes/', create_note),
    path('upload_question_paper/', create_question_paper),
    path('view_notes/', view_notes),
    path('get_question_paper/', get_question_paper),
    

    # token refresh for authnetication
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]