from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    #so now i need to make this validateRegistration work: and need to pass in that form_data argument
    def validateRegistration(self, form_data):
    #now i need to check for required
        errors = []

        if len(form_data['first_name']) == 0:
            errors.append("First Name is required.")
        if len(form_data['last_name']) == 0:
            errors.append("Last Name is required.")
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        if form_data['password'] != form_data['password_confirmation']:
            errors.append("Passwords do not match.")
        
        return errors
    #now go to views and insert "if not errors:" for verification

    def validateLogin(self, form_data):
        errors = []
#also check to see if user exists in DB. see views

        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) == 0:
            errors.append("Password is required.")

        return errors

    #insert 'createUser' method here
    def createUser(self, form_data):
    #bcrypt step 1: is to convert user password to a str
    #password is the str form of password
        password = str(form_data['password'])
    #step 2: we need to hash that password copy and past this line: "hashed = bcrypt.hashpw(password, bcrypt.gensalt())"
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        #here is going to be all the keys and their values
        user = User.objects.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            #so instead of saving the password to our form = "form_data['password']" we are going to save the hashed_pw
            password = hashed_pw,
            #now we are going to store this in session in views
        )

        return user
        #now we are goin to do bcrypt from here (also ref platform)
        #bcryt has installed successfully, now just import at top of this page.
class WishManager(models.Manager):
    def validate(self, form_data):
        
        def createWish(self, form_data, user):
            wish = Wish.objects.create(
                content = form_data['content'],
                user = user,
            )

            return wish

class Wish(models.Model):
    user = models.ForeignKey(User, related_name="wishes")
    content = models.TextField()
    added_by = models.ManyToManyField(User, related_name="same_wish")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AuthorManager(models.Manager):
    def createAuthor(self, form_data):
        name = form_data['name']
        author = Author.objects.create(name=name)
        
        return author

class Author(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#these two classes are currently not attatched so I am going to need a relationship between them.
#need to validate date using this model manager. classname then Manager.
    objects = AuthorManager()

    objects = WishManager()