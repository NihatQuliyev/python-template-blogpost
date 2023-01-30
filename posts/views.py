from django.shortcuts import render,get_object_or_404
from django.db.models import Q 
from .models import Category, Post, Author , Exam ,Comment
from taggit.models import Tag 
from .forms import CommentForm


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]


    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.save()
        comment_form = CommentForm()


    context = {
        'post': post,
        'latest': latest,
        'post':post,'comments': comments,
        'comment_form':comment_form
    }
    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')

#exam
def exam (request):
    exam = Exam.objects.get()

    context = {
        'exam': exam
    }

    return render(request, 'exam.html',context)

def search(request):
    queryset = Post.objects.all()
    querysetexam = Exam.objects.all()
    query = request.GET.get('q')
    if query:
        querysetexam = querysetexam.filter(
            Q(name__icontains=query) |
           	Q(surname__icontains=query) |
            Q(qroup__icontains=query) |
            Q(email__icontains=query) 
            
        ).distinct()



        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset,
        'exam_list' : querysetexam   #go shorcbar
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)




def post_list(request, tag_slug=None):

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])

        context ={
                'posts':posts,
                'tag':tag
        } 

    
    return render(request,'post_list.html',context)



# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))

    return redirect("/")



#Author
def postlist_author (request,author_id):
    posts = Post.objects.filter(author_id=author_id).order_by('-timestamp')
    author = Author.objects.get(user_id = author_id)

    context = {
        'posts': posts,
        'author' : author,

    }
    return render(request, 'author.html', context)