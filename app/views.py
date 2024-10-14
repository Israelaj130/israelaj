from django.shortcuts import render, redirect, reverse
from app.models import Blog, Comment
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
# Create your views here.

def homepage(request):
    all_products=['Tote bag', 'perfume','jewelries']
    context={"products": all_products}
    return render(request, 'app/index.html', context)
def about(request):
    return render(request, 'app/about.html')
def hello(request):
    return render(request,'app/contact.html')

@login_required
def blogs(request):
    user= request.user
    my_blogs= Blog.objects.filter(owner=user).order_by("-created_at")[:5]
    other_blogs= Blog.objects.all().exclude(owner = user).order_by("-created_at")[:5]
    context={'my_blogs': my_blogs, "other_blogs": other_blogs}
    return render(request, 'app/blogs.html', context)

@login_required
def read(request,id):
    single_blog=Blog.objects.filter(id=id).first()
    user= request.user
    if not single_blog:
        messages.error(request, "Invalid blog")
        return redirect(blogs)
    blog_comments= Comment.objects.filter(blog=single_blog).order_by('-created_at')
    context={"blog":single_blog, 'comments': blog_comments}
    if request.method == "POST":
        body= request.POST.get('comment')
        if not body:
            messages.error(request, "comment can not be empty")
            return redirect(reverse("read", kwargs={'id':id}))
        Comment.objects.create(
            owner= user,
            blog= single_blog,
            body= body
        )
        return redirect(reverse("read", kwargs={'id':id}))
    return render(request, 'app/read.html', context)

def delete(request, id):
    single_blog= Blog.objects.filter(id=id).first()
    user= request.user
    if not single_blog:
        messages.errpr(request, 'invalid blog')
        return redirect(blogs)
    if single_blog.owner != user:
        message.error(request, "Unauthorized access")
        return redirect(blogs)
    single_blog.delete()
    messages.success(request, "Blog deleted successfully")
    return redirect (blogs)
@login_required
def create(request):
    user= request.user
    if request.method =='POST':
        title=request.POST.get('title')
        body=request.POST.get('body')
        image=request.FILES.get('image')
        dsc=request.POST.get('description')
        if not title or not body or not image:
            messages.error(request, "field compulsory")
            return redirect(create)
        if len(title)>250:
            messages.error(request, "title is too long")
            return redirect(create)
        Blog.objects.create(
            title=title,
            body=body,
            image=image,
            description=dsc,
            owner=user
        )
        messages.success(request,"Blog created successful")
        return redirect(homepage)
    return render(request, 'app/create.html')
@ login_required
def edit(request,id):
    single_blog=Blog.objects.filter(id=id).first()
    user= request.user
    if not single_blog:
        messages.error(request, "Invalid blog")
        return redirect(blogs)
    if single_blog.owner != user:
        messages.error(request, "Unauthorized access")
        return redirect(blogs)
    context={"blog":single_blog}
    if request.method=='POST':
        title=request.POST.get("title")
        body=request.POST.get("body")
        image=request.POST.get("image")
        description=request.POST.get("description")
        if not title or not body:
            messages.error(request, "field compulsory")
            return redirect(create)
        if len(title) > 250:
            messages.error(request, "title is too long")
            return redirect(create)
        single_blog.title=title
        single_blog.body=body
        single_blog.description=description

        if image:
            single_blog.image=image
        single_blog.save()
        messages.success(request,"blog updated")
        return redirect(homepage)
    return render(request, "app/edit.html", context)

def signup(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        if not username or not email or not firstname or not lastname or not password or not cpassword:
            messages.error(request, "All fields required")
            return redirect(signup)
        if password != cpassword:
            messages.error(request, "password is not the same")
            return redirect(signup)
        if len(password)< 8:
            messages.error(request, "password not up to 8 characters")
            return redirect(signup)
        if len(username)< 8:
            messages.error(request, "username not up to 8 characters")
            return redirect(signup)
    
        username_exists= User.objects.filter(username=username).exists()

        if username_exists:
            messages.error(request, "username already exist")
            return redirect(signup)
        email_exists=User.objects.filter(email=email).exists()
        if email_exists:
            messages.error(request, "email already exist")
            return redirect(signup)
        user=User.objects.create(
            username=username,
            email=email,
            first_name=firstname,
            last_name=lastname
        )
        user.set_password(password)
        user.save()
        messages.success(request, "successful")
        return redirect(homepage)
    return render(request, 'app/form.html')

def login(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    next=request.GET.get('next')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not username or not password:
            messages.error(request, "All field required")
            return redirect(login)
        user=auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, "Invalid login credentials")
            return redirect(login)
        auth.login(request,user)
        return redirect(next or homepage)
    return render (request, 'app/login.html')

def logout(request):
    auth.logout(request)
    return redirect(login)
