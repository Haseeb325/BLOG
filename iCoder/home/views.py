from django.shortcuts import render
from django.shortcuts import HttpResponse , redirect
from .models import *
from blog.models import Post
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout

# Create your views here.

# HTML Pages

def home(request):
    return render(request , 'home/home.html')

def contact(request):
    if request.method =="POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        content = request.POST.get('content')

        queryset = Contact.objects.all()
        if len(name)<2 or len(email)<2 or len(content)< 4:
         messages.error(request, "Please Enter details bit lengthy")
        else: 
         queryset.create(
            name = name,
            email = email,
            phone = phone,
            content = content
          )
         messages.info(request , "Account Created Successfully")
         return redirect('/contact')

    return render(request , 'home/contact.html')

def about(request):
    return render(request , 'home/about.html')

def search(request ,):
    search = request.GET['search']
    if len(search)>30:
        # make empty queryset This is for 1st method of giving  but 2nd is working good
    #    allPosts =Post.objects.none()
  

    #    2nd metod of giving message
       allPosts =[]
       messages.error(request, "Please Enter details bit small query search")
    
    else:
        #   first method 
        #   allPosts = Post.objects.all()
        #   allPosts = allPosts.filter(
        #   Q(title__icontains =search)|
        #   Q(content__icontains =search)
        #    )

        #   2nd method
            allPostsTitle = Post.objects.filter(title__icontains = search) 
            allPostsContent = Post.objects.filter(content__icontains = search) 
            allPosts = allPostsTitle.union(allPostsContent)

           #  1st method of message 
    # if allPosts.count() == 0:
    #    messages.error(request, "Please Enter details bit small query search")

    params ={"allPosts":allPosts , "search": search}
    return render (request, 'home/search.html' ,params)
    # return HttpResponse("This is search")



#  Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        # request.post 1 dictionary hai jisko mai query kr rha hun us mai main username jo meri key hai us k corresponding value ko lekr username mai store kr rha hun
      username = request.POST['username']
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      email = request.POST['email']
      password1 = request.POST['password1']
      password2 = request.POST['password2']

      #  Checks For errorneous inputs
      if len(username) > 10:
          messages.error(request, "Username must be under 10")
          return redirect("/")
      if not username.isalnum():
          messages.error(request, "Username must be contains letters and numbers")
          return redirect("/")
         
      if password1 != password2:
         messages.error(request, "Password must match each other")
         return redirect("/")           

      # Create the User
      myuser = User.objects.create_user(username , email, password1)
      myuser.first_name = firstname
      myuser.last_name = lastname
      myuser.save()
      messages.success(request, "Your account has been created successfully")
      return redirect("/")

    else:
        return HttpResponse("404 - Not Found")    
    

def handleLogin(request):

   if request.method == "POST":
    loginusername = request.POST['loginusername']
    loginpassword = request.POST['loginpassword']
    
    user = authenticate(username  = loginusername , password =  loginpassword)

    if user is not None:
       login(request, user)
       messages.success(request, "Successfully Logged In")
       return redirect("/")

    else:
       messages.error(request , "Invalid Credentials")
       return redirect("/")
          

   return HttpResponse("404 - Not-Found")


def handleLogout(request):
   
    # if request.method =="POST":
       logout(request)
       messages.success(request , "Successfully Logged Out")
       return redirect("/")

       return HttpResponse("Logout")



#     Comments    
