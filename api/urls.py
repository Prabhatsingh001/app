"""API URL routes for the project.

This module wires together the project endpoints exposed under the API prefix.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from CgCalculator.views import CGPACalculatorView
from feedback.views import FeedbackAPI
from studybudy import views
from UploadNotesOrQuestionPaper.views import (
    create_note,
    create_question_paper,
    get_question_paper,
    view_notes,
)

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("change_password/", views.change_password, name="change_password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update_profile/", views.Update_Profile, name="update_profile"),
    path("delete_profile/", views.delete_profile, name="delete_profile"),
    path(
        "delete_profile_picture/",
        views.delete_profile_picture,
        name="delete_profile_picture",
    ),
    path("upload_notes/", create_note, name="upload_notes"),
    path("upload_question_paper/", create_question_paper, name="upload_question_paper"),
    path("view_notes/", view_notes, name="view_notes"),
    path("get_question_paper/", get_question_paper, name="get_question_paper"),
    path("feedback/", FeedbackAPI.as_view(), name="feedback"),
    path("calculate-cgpa/", CGPACalculatorView.as_view(), name="calculate-cgpa"),
]
