from django.db import models
import re
import bcrypt
from datetime import date

class UserManager(models.Manager):
    #register validation
    def reg_validation(self,data):
        errors={}

        firstname=data['firstname']
        lastname=data['lastname']
        email=data['email']
        password=data['password']
        confirm_pw=data['confirm_pw']

        if len(firstname) == 0:
            errors['firsnameerror']="firstname is required"
        if len(lastname) == 0:
            errors['lastnameerror']="lastname is required"
        if len(email) == 0:
            errors['emailerror']="email is required"
        if len(password) == 0:
            errors['passworderror']="password is required"
        if len(firstname) < 2:
            errors['firsnameerror']="firstname must be at least 2 chars"
        if len(lastname) < 2:
            errors['lastnameerror']="lastname must be at least 2 chars"
        if len(password) < 8:
            errors['passworderror']="password must be at least 8 chars"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if email and not EMAIL_REGEX.match(email):
            errors['emailerror']="email is invalid"

        if password != confirm_pw :
            errors['confirm_pwerror']="passwords do not match"

        if email and User.objects.filter(email=email).exists():
            errors['emailerror']="email already exists"

        return errors


    def create_user(self,data):
        firstname=data['firstname']
        lastname=data['lastname']
        email=data['email']
        password=data['password']
        

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user=User.objects.create(firstname=firstname,lastname=lastname,email=email,password=pw_hash)

        return user

    def login_validation(self,data):
        errors={}

        email=data['email']
        password=data['password']

        if len(email) == 0:
            errors['loginemailerror']="email is required"
        if len(password) == 0:
            errors['loginpassworderror']="password is required"

        if len(errors) == 0 :
            user = User.objects.filter(email=email)
            if user :
                logged_user=user[0]

                if not bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                   errors['loginerror']="invalid email or paswword"
            #when user does not exist
            else:
                errors['loginerror']="invalid email or paswword"

        return errors

    def login_user(self,data):

        email=data['email']
        password=data['password']
        user=User.objects.get(email=email)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        return None
    
class IdeaManager(models.Manager):
    #idea validation
    def idea_validation(self,data):
        errors={}
        idea=data['idea']
      

        if len(idea) == 0:
            errors['ideaerror']="idea is required"
        
        elif len(idea) < 5:
            errors['ideaerror']="idea must be at least 3 chars"
       
        return errors

    def create_idea(self, data, user):

        idea = Idea.objects.create(
            idea = data["idea"],
            user=user
        )

        return idea
    

    def update_idea(self,data,idea):
        idea.idea=data['idea']
        idea.save()
        

class User(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    objects=UserManager()

class Idea(models.Model):
    idea=models.CharField(max_length=255)
    user=models.ForeignKey(User,related_name="ideas",on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    objects=IdeaManager()
