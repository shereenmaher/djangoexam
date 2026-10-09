from django.urls import path
from . import views

urlpatterns = [
    path('', views.reg_log_page),
    path('register', views.register),
    path('login', views.login),

    path('ideas', views.ideas),
    path('create_idea', views.create_idea),
    path('view_idea/<int:idea_id>', views.view_idea),
    path('edit_idea/<int:idea_id>', views.edit_idea,name="editidea"),
    path('delete_idea/<int:idea_id>', views.delete_idea),
   
    path('logout', views.logout),
]
