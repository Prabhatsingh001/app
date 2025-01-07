from studybudy import views
from UploadNotesOrQuestionPaper.views import create_note, create_question_paper, view_notes, get_question_paper
from feedback.views import FeedbackAPI
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from CgCalculator.views import CGPACalculatorView

# urlpatterns = [
#     # signup login and logout
#     path('signup/', views.signup,name='signup'),
#     path('login/', views.login,name='login'),
#     path('logout/', views.logout,name='logout'),
#     path('delete_profile_picture/', views.delete_profile_picture, name='delete_profile_picture'),

#     # forgot password and change password
#     path('change_password/', views.change_password,name='change_password'),

#     # dashboard and profile
#     path('dashboard/', views.dashboard,name='dashboard'),
#     path('update_profile/', views.Update_Profile,name='update_profile'),
#     path('delete_profile', views.delete_profile,name='delete_profile'),
    
#     # upload notes and question paper
#     path('upload_notes/', create_note,name='upload_notes'),
#     path('upload_question_paper/', create_question_paper,name='upload_question_paper'),
#     path('view_notes/', view_notes,name='view_notes'),
#     path('get_question_paper/', get_question_paper,name='get_question_paper'),
    
#     # feedback
#     path('feedback/', FeedbackAPI.as_view(),name='feedback'),


#     # token refresh for authentication
#     path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
# ]

auth_patterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]

profile_patterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_profile/', views.Update_Profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('delete_profile_picture/', views.delete_profile_picture, name='delete_profile_picture'),
]

notes_patterns = [
    path('upload_notes/', create_note, name='upload_notes'),
    path('upload_question_paper/', create_question_paper, name='upload_question_paper'),
    path('view_notes/', view_notes, name='view_notes'),
    path('get_question_paper/', get_question_paper, name='get_question_paper'),
]

feedback_patterns = [
    path('feedback/', FeedbackAPI.as_view(), name='feedback'),
]

urlpatterns = (
    auth_patterns
    + profile_patterns
    + notes_patterns
    + feedback_patterns
    + [
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]+[
    path('calculate-cgpa/', CGPACalculatorView.as_view(), name='calculate-cgpa'),
]
)
