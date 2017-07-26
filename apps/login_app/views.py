from django.shortcuts import render, redirect, reverse
#incorporating 'named routes' use this reverse (i.e. '/success' changes to:
#   return redirect(reverse('success'))
#below import messages is coppied & pasted from external site: https://docs.djangoproject.com/en/1.11/ref/contrib/messages/
from django.contrib import messages
import bcrypt
#before I can use my User model I need to import it in
from .models import User

# Create your views here.
def flashErrors(request, errors):
    for error in errors:
    #copy from external site : messages.error(request, 'Document deleted.')
        messages.error(request, error)
        #so now instead of printing errors, we can say: flashErrors(request, errors)

# def currentUser(request):
#     id = request.session['user_id']
# #this will return the current user from my DB
#     return User.objects.get(id=id) this being moved to models inside login_app for more virsatile usability

def index(request):

    return render(request, 'login_app/index.html')

def success(request):
#"if 'user_id' in request.session:" this is checking to see if there is something inside request session, if not redirect back /
    if 'user_id' in request.session:
        #i want to get all the users but myself
        current_user = User.objects.currentUser(request)
    #ORM i want all users who are not me: exclude
        # users = User.objects.exclude(id=current_user.id) now that i have my ORM set I am changing this line to get all the users whom are NOT my friends to the line below
        friends = current_user.friends.all()
        #exclude(id__in - means user objects not id in...
        users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)
#***Context: this key users is the only thing that matters in the html {% for user in users %} from form_data
        context = {
            'users': users,
            'friends': friends,
        }
                            #DONT FORGET TO ADD CONTEXT HERE!!!!
        return render(request, 'login_app/success.html', context)
    #else let's redirect back and login and register
    return redirect(reverse('landing'))

def register(request):
    if request.method == "POST":
    #validate method in errors variable & pass in (form_data)
    #so now I need to go make this validateRegistration 
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            #so if I didn't get any issues with the data, it was all inserted correctly, then I am goin to take in that data and create a user
            #so now i am going use another custom model method to do that for me
            user = User.objects.createUser(request.POST)
            #so now i am going to create this method 'createUser'
            #pw stored in session
            request.session['user_id'] = user.id

            return redirect(reverse('success'))
    #if there are errors we will print them for a moment and then redirect to home page
        # print errors, now this changes to flashErrors(request, errors)
        flashErrors(request, errors)

    return redirect(reverse('landing'))
    

def login(request):
#dont forget to wrap all of the below in this post method
    if request.method == "POST":
#this will be pretty similar to register method we need to validate some data. catch the errors and pass in the form_data=(request.POST)
        errors = User.objects.validateLogin(request.POST)
        #now let's go build that method 'validateLogin'
        if not errors:
            user = User.objects.filter(email = request.POST['email']).first()

            #"if user:"- means that user does exist
            if user:
            #check for password matching , need to import bcrypt at top of this page. below we check the matching str that exists in our DB
                password = str(request.POST['password'])
                user_password = str(user.password)

                hashed_pw = bcrypt.hashpw(password, user_password)
                #so now we can check to see if hashed pw and user pw are correct
                if hashed_pw == user.password:
                    #if all info is correct then we need to log user in
                    request.session['user_id'] = user.id

                    return redirect(reverse('success'))
                #if login effort was incorrect then "invalid login info"
            errors.append("Invalid account information.")

        flashErrors(request, errors)

    return redirect(reverse('landing'))            

def logout(request):
    if 'user_id' in request.session:
        #if there is something in session then we will pop out that key id from DB
        request.session.pop('user_id')

    return redirect(reverse('landing'))

def addFriend(request, id):
    #always have to have this method
    if request.method == "POST":
        #now we need to make sure user is logged in
        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)
        #ORM current user to friend (many to many field)
        #start from one user access the relationship and add to the other
        #I want to take my current user / access my friends relationship / & add a new friend to it.
            current_user.friends.add(friend)
#.add is only used on a M:M field, everything else is create....
# i.e. Post.objects.create(content='I have a life, yay!', user=current_user)
            return redirect(reverse('success'))

    return redirect(reverse('landing'))

def removeFriend(request, id):
    #always have to have this method
    if request.method == "POST":
        #now we need to make sure user is logged in
        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)
        #ORM current user to friend (many to many field)
        #start from one user access the relationship and add to the other
        #I want to take my current user / access my friends relationship / & add a new friend to it.
            current_user.friends.remove(friend)

            return redirect(reverse('success'))

    return redirect(reverse('landing'))