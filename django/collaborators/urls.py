from django.urls import path
from .views import CollaboratorSignupView


app_name = 'collaborators'

urlpatterns = [

    # APIs V1
    path('signup/', CollaboratorSignupView.as_view(), name='v1_signup'),

    # APIs V2


    # APIs V3

]