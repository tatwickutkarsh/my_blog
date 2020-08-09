from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import Post,Comment,Profile
from  .forms import PostForm,CommentForm,RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth import login

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'blog/post_list.html', { 'posts' : posts })
   
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', { 'post' : post })

@login_required
def post_new(request):
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES or None)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            #post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', { 'form' : form})

@login_required
def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk,author=request.user)
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES or None,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            if post.published_date != None:
                post.edited_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', { 'form' : form})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True, author=request.user).order_by('created_date')
    return render(request, 'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk,author=request.user)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_delete(request,pk):
    post=get_object_or_404(Post,pk=pk,author=request.user)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid:
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:        
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form' : form} )  

@login_required
def remove_comment(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if comment.post.author == request.user:
        comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def approve_comment(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if comment.post.author == request.user:
        comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
    
def register(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            form=RegisterForm(initial={'profile_pic':request.user.profile.prof_pic},instance=request.user)
        else:    
            form=RegisterForm()
        return render(request,'registration/register.html',{'form':form})
        
    else:
        form=RegisterForm(request.POST,request.FILES)
        if request.user.is_authenticated:
            #print("Hello")
            prof_pic=request.FILES.get('profile_pic',None)
            password2=request.POST.get('password2')
            password1=request.POST.get('password1')
            #print(password1,password2,request.user.password,sep='\n')
            flag=0
            #if password is None:
            #=request.POST.pop('password1')
            #request.POST['password']="1234"
            for x in request.user._meta.fields:
                if (x.name in request.POST.keys()) and (x.name != 'username'):
                    temp=getattr(request.user,x.name)
                    if  (temp != request.POST[x.name]):
                        if (x.name not in form.errors.keys()):
                            setattr(request.user,x.name,request.POST.get(x.name,temp))
                        else:
                            #print(x.name)
                            form.initial={'profile_pic':request.user.profile.prof_pic}
                            return render(request,'registration/register.html',{'form':form})   
            if prof_pic != None:
                if prof_pic != request.user.profile.prof_pic:
                    request.user.profile.prof_pic= prof_pic
                    request.user.profile.save()
            if (password1==password2) and (password1!='') and(password1!=request.user.password):
                request.user.set_password(password1)
                flag=1
            elif password1 != password2:
                #password1=request.user.password
                #password2=request.user.password
                form.initial={'profile_pic':request.user.profile.prof_pic}
                return render(request,'registration/register.html',{'form':form})       

            pk=request.user.pk    
            request.user.save()
            if flag:
                user=User.objects.get(pk=pk)      
                login(request,user)   
            return redirect('profile')   
        else:
            #form=RegisterForm(request.POST,request.FILES)
            if form.is_valid():
                prof_pic=form.cleaned_data.pop('profile_pic')
                form.cleaned_data.pop('password2')
                form.cleaned_data['password']=form.cleaned_data.pop('password1')
                author=User.objects.create_user(**form.cleaned_data)
                Profile.objects.create(user=author,prof_pic=prof_pic)
                login(request,author)
                return redirect('post_list')
    
        return render(request,'registration/register.html',{'form':form})    

def profile(request):
    return render(request,'blog/profile.html')    

def blogger_list(request):
    users=User.objects.all()
    bloggers=[]
    for blogger in users:
        if len(blogger.post_set.all()):
            bloggers.append(blogger)

    def fnc(x):
        ans=0
        for y in x.post_set.all():
            if y.published_date != None:
                ans+=1
        return ans
    
    sorted(bloggers,key=fnc,reverse=True)
    return render(request,'blog/blogger_list.html',{'bloggers':bloggers})

def blogger_detail(request,pk):
    blogger=get_object_or_404(User,pk=pk)
    if request.user != blogger:
        posts=blogger.post_set.filter(published_date__isnull=False)
        return render(request,'blog/blogger_detail.html',{'blogger':blogger,'posts':posts})
