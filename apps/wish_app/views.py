from django.shortcuts import render, redirect, reverse
# from django.db.models import Count
from ..login_app.models import User
from .models import Wish

def index(request):
    wish = Wish.objects.all()
    current_user = User.objects.currentUser(request)
    # wish = Wish.objects.annotate(num_likes=Count('liked_by'))

    context = {
        'user': current_user,
        'wish': wish,
    }

    return render(request, 'wish_app/index.html', context)

def create(request, id):
    print "Inside the create method."
    current_user = User.objects.currentUser(request.POST, id)
    wish = Wish.objects.get(id=id)
    if request.method == "POST":

        if len(request.POST['content']) != 0:
            current_user = User.objects.currentUser(request)
            #so if content is not empty then lets create a secret method
            wish = Wish.objects.createWish(request.POST, current_user)

    return redirect('success')

def share(request, id):
    print "Inside the share method."
    current_user = User.objects.currentUser(request)
    wish = Wish.objects.get(id=id)
    if request.method == "POST":

        if len(request.POST['content']) != 0:
            current_user = User.objects.currentUser(request)
            #so if content is not empty then lets create a secret method
            shared = Share.objects.shareWish(request.POST, current_user)

    return redirect(reverse('success'))
#so now we just need to relate the two tables = .add method..
#to get to the relationship from the Secret it would be = Secret.liked_by
#to get to the rel from the User it would be = User.likes
#one way: current_user.likes.add(secret) & another way secret.liked_by.add(current_user)

def delete(request, id):
    if request.method == "POST":
        wish = Wish.objects.get(id=id)
        current_user = User.objects.currentUser(request)
# if the user matches the same id of the secret post id 
        if current_user.id == wish.user.id:
            wish.delete()

    return redirect(reverse('success'))
