from studybudy.views import people,people_update,partial_update_person,people_delete,signup,login,dashboard,Update_Profile
from django.urls import path


urlpatterns = [
    path('login/', login),
    path('signup/', signup),
    path('dashboard/', dashboard),
    path('update_profile/',Update_Profile),


    path('people/', people),
    path('people/<int:id>/', people_update),
    path('people_delete', people_delete),
    path('people/<int:id>/', partial_update_person)
]