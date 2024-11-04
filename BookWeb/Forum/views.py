from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage

from UserAuth.models import User
from Groups.models import Village,Experience
from .models import Topic, Post, GTopic, GPost
from .forms import NewTopicForm, PostForm, NewGTopicForm, GPostForm
import math  

import re
import os


def get_matching_files(request):
    pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    file_names = os.listdir(settings.PROFILE_ROOT)
    matching_files = []
    for file_name in file_names:
        if pattern.match(file_name):
            matching_files.append(file_name)
    # 没有上传就用默认的
    if not matching_files:
        matching_files.append('default.png')
    return matching_files[0]


# Create your views here.
def home(request):
    
    topics = Topic.objects.order_by('last_updated')
    if 'search' in request.GET:
        search_query = request.GET['search']
        topics = Topic.objects.filter(subject__icontains=search_query)

    topics_per_page = 20
    paginator = Paginator(topics, topics_per_page)
    page_number = request.GET.get('page')

    try:
        current_page = paginator.get_page(page_number)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        'matching_files': get_matching_files(request),
        'topics': current_page,
        'page_size': topics_per_page,
    }
    return render(request, 'Forum/home.html', context)


def new_topic(request):
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.starter = User.objects.get(pk=request.session['UserInfo'].get('id'))
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=topic.starter
            )
            return redirect('Forum:topic_posts', pk=topic.pk)

    else:
        form = NewTopicForm()

    context = {
        'form': form,
        'matching_files': get_matching_files(request),
    }
    return render(request, 'Forum/new_topic.html', context)


def topic_posts(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.views += 1
    topic.save()

    context = {
        'topic': topic,
        'matching_files': get_matching_files(request),
    }

    return render(request, 'Forum/topic_posts.html', context)


def reply_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = User.objects.get(pk=request.session['UserInfo'].get('id'))
            post.save()
            return redirect('Forum:topic_posts', pk=pk)
    else:
        form = PostForm()
    return render(request, 'Forum/reply_topic.html', {'topic': topic, 'form': form})


def Ghome(request,gpk):
    gtmp_id=gpk
    #print(gpk)
    #print(tmp_id)
    query_set = Village.objects.filter(id=gpk)
    obj=query_set.first()
    Gtopics = obj.gtopics.order_by('last_updated') 
    
    Gtopics_per_page = 20
    paginator = Paginator(Gtopics, Gtopics_per_page)
    page_number = request.GET.get('page')

    try:
        current_page = paginator.get_page(page_number)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    tmp_id=request.session['UserInfo'].get("id")
    user_query=User.objects.filter(id=tmp_id)
    user=user_query.first()
    identity=0
    if(obj.admin.username==user.username):
        identity=1
    context = {
        'matching_files': get_matching_files(request),
        'topics': current_page,
        'page_size': Gtopics_per_page,
        'identity':identity,
        'gid':gtmp_id
    }
    #print(gtmp_id)
    return render(request, 'Forum/ghome.html', context)

def new_gtopic(request):
    if request.method == 'POST':
        form = NewGTopicForm(request.POST)   # check whether the form function needs to be changed
        if form.is_valid():
            gtopic = form.save(commit=False)
            gtopic.group = Village.objects.get(pk=request.session['GroupInfo'].get('id'))
            gtopic.starter = User.objects.get(pk=request.session['UserInfo'].get('id'))
            gtopic.save()
            thestarter=User.objects.get(pk=request.session['UserInfo'].get('id'))
            thegroup= Village.objects.get(pk=request.session['GroupInfo'].get('id'))
            query_set=Experience.objects.filter(user=thestarter,admin=thegroup)
            exp=query_set.first()
            exp.experience+=1
            exp.save()
            post = GPost.objects.create(
                message=form.cleaned_data.get('message'),
                topic=gtopic,
                created_by=gtopic.starter
            )

            return redirect('Forum:group_posts', pk=gtopic.pk)

    else:
        form = NewGTopicForm()

    context = {
        'form': form,
        'matching_files': get_matching_files(request),
    }
    return render(request, 'Forum/new_gtopic.html', context)   #I think zhelibuyonggai


def gtopic_posts(request, pk):
    gtopic = get_object_or_404(GTopic, pk=pk)
    gtopic.views += 1
    gtopic.save()
    gid=request.session['UserInfo'].get('id')
    thestarter=User.objects.get(pk=request.session['UserInfo'].get('id'))
    thegroup= Village.objects.get(pk=request.session['GroupInfo'].get('id'))
    query_set=Experience.objects.filter(user=thestarter,admin=thegroup)
    exp=query_set.first()
    expnum=exp.experience+1
    level=math.log2(expnum)
    level=math.floor(level)
    flag4=flag1=flag3=flag5=flag2=False
    if level<=1:
        flag1=True
    elif level==2: 
        flag2=True
    elif level==3: 
        flag3=True
    elif level==4: 
        flag4=True
    elif level>=5:
        flag5=True
    
    context = {
        'topic': gtopic,
        'matching_files': get_matching_files(request),
        'gid': gid,
        'level':level,
        'flag1':flag1,
        'flag2':flag2,
        'flag3':flag3,
        'flag4':flag4,
        'flag5':flag5
    }

    return render(request, 'Forum/gtopic_posts.html', context)


def reply_gtopic(request, pk):
    gtopic = get_object_or_404(GTopic, pk=pk)
    if request.method == 'POST':
        form = GPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = gtopic
            post.created_by = User.objects.get(pk=request.session['UserInfo'].get('id'))
            post.save()
            thestarter=User.objects.get(pk=request.session['UserInfo'].get('id'))
            thegroup= Village.objects.get(pk=request.session['GroupInfo'].get('id'))
            query_set=Experience.objects.filter(user=thestarter,admin=thegroup)
            exp=query_set.first()
            print(exp.user.username)
            print(exp.experience)
            exp.experience=exp.experience+1
            print(exp.experience)
            exp.save()
            return redirect('Forum:group_posts', pk=pk)
    else:
        form = PostForm()
    return render(request, 'Forum/reply_topic.html', {'topic': gtopic, 'form': form})
