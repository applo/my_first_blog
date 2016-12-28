from django.shortcuts import render
from .models import Post
from django.utils import timezone
from .form import PostForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)     #  获取视图或者404
    print("post:")
    print(post)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":  # 如果post了一个表格（还是向同一个页面post的，就会调用if后面的语句）

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            print('-------------')
            print(post.pk)
            print(post)

            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    print('now show the html')
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)   #instance用来明确被修改的对象
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})