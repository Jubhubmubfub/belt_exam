from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
import south

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateReg(self,request):
        errors = self.validate_inputs(request)
        if errors:
            return (False,errors)
        user_list = User.objects.filter(email=request.POST['email'].lower())
        if len(user_list)>0:
            errors.append("Email already exists")
            return (False, errors)
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            user = self.create(first_name=request.POST['first_name'],alias=request.POST['alias'],email=request.POST['email'].lower(),pw_hash=pw_hash)
            return (True,user)


    def validateLogin(self, request):
        errors = []
        user_list = User.objects.filter(email=request.POST['email'].lower())
        if len(user_list)<1:
            errors.append("Email/Password doesn't match!")
            return (False, errors)
        else:
            password = request.POST['password'].encode()
            if user_list[0].pw_hash == bcrypt.hashpw(password,user_list[0].pw_hash.encode()):
                return (True,user_list[0])
            else:
                errors.append("Email//Password doesn't match!")
                return (False,errors)

    def validate_inputs(self, request):
        errors = []
        if len(request.POST['first_name']) < 3 or len(request.POST['alias']) < 3:
            errors.append("Please enter a first name/alias that is longer than 2 characters")
        elif request.POST['first_name'].isalpha() == False:
            errors.append("Only use letter characters for First name field")
        if len(request.POST['email'])<1:
            errors.append("Please enter an email")
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Invalid email entered")
        if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['confirm_pw']:
            errors.append("Passwords must match and be at least 8 characters.")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
