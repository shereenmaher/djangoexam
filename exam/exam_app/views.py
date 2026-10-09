from django.shortcuts import render , HttpResponse,redirect
from .models import *
from .import models


def reg_log_page(request):
    return render(request,"reg_log.html")

def register(request):
    if request.method == 'POST':

        errors=User.objects.reg_validation(request.POST)

        if len(errors) > 0 :
            context={
                "errors":errors
            }
            return render(request,"reg_log.html",context)

        else:
            user=User.objects.create_user(request.POST)
            request.session['user_id']=user.id

            return redirect("/ideas")

    else:
        return redirect("/")

def login(request):
    if request.method == 'POST':
    
            errors=User.objects.login_validation(request.POST)
    
            if len(errors) > 0 :
                context={
                    "errors":errors
                }
                return render(request,"reg_log.html",context)
            else:
                user=User.objects.login_user(request.POST)
                request.session['user_id']=user.id
            return redirect("/ideas")
    else:
        return redirect("/")

def ideas(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        user=User.objects.get(id=request.session['user_id'])
        ideas=Idea.objects.all()

        context={
            "user":user,
            "ideas":ideas
        }
        return render(request,"ideas.html",context)

def create_idea(request):

    if "user_id" not in request.session:

        return redirect("/")

    else:

        user = User.objects.get(
            id=request.session["user_id"]
        )

        if request.method == "POST":

            errors = Idea.objects.idea_validation(request.POST)

            if len(errors) > 0:

                context = {
                    "user": user,
                    "errors": errors
                }

                return render(request,"ideas.html",context)

            else:
                user = User.objects.get( id=request.session["user_id"] )
                Idea.objects.create_idea(request.POST,user)

                return redirect("/ideas")

        else:

            context = {
                "user": user
            }

            return render(request,"ideas.html",context)


def view_idea(request,idea_id):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        user=User.objects.get(id=request.session['user_id'])

        idea=Idea.objects.get(id=idea_id)

        context={
            "user":user,
            "idea":idea
        }
        return render(request,"view.html",context)

def edit_idea(request,idea_id):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        user=User.objects.get(id=request.session['user_id'])

        idea=Idea.objects.get(id=idea_id)

        if idea.user.id != user.id:
            return redirect("/")

        if request.method == 'POST': 
            errors=Idea.objects.idea_validation(request.POST)
            if len(errors) > 0 :
                context={
                    "user":user,
                    "idea":idea,
                    "errors":errors
                }
                return render(request,"edit.html",context)
            else:
                Idea.objects.update_idea(request.POST,idea)
                return redirect("/ideas")
        else:
            context={
                "user":user,
                "idea":idea,
            }
            return render(request,"edit.html",context)

def delete_idea(request,idea_id):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        user=User.objects.get(id=request.session['user_id'])
    
        idea=Idea.objects.get(id=idea_id)
        if idea.user.id == user.id:
            idea.delete()
        return redirect("/ideas")


def logout(request):
    request.session.flush()
    return redirect("/")

