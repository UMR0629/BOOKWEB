from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from Groups.utils.forms import CreateForm
from UserAuth.models import User
from django.shortcuts import render, HttpResponse, redirect
from Groups.models import Village,Experience
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404 
from Apply.models import Application
import re
import json 
# Create your views here.
def create(request):
    if request.method=='GET':
        form = CreateForm(request=request)
        context = {
            'form': form,
            'nid': 1  # represent registration
        }
        return render(request, 'create.html', context=context)
    form = CreateForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
            'nid': 1
        }
        return render(request, 'create.html', context=context)
    tmp_id=request.session['UserInfo'].get("id")
    if tmp_id==None:
        return redirect("/info/info/")
    theuser = User.objects.get(id=tmp_id)
    #form.admin_id= request.session['UserInfo'].get("id")
    form.instance.admin=theuser
    group=form.save()
    group.members.add(theuser)
    Experience.objects.create(experience=0, admin=group, user=theuser ) 
    return redirect("/")

def show(request):
    
    villages = Village.objects.order_by('villagename')  #这里看看要不要根据群组人数什么的进行排序
    if 'search' in request.GET:
        search_query = request.GET['search']
        villages = Village.objects.filter(subject__icontains=search_query)

    villages_per_page = 20
    paginator = Paginator(villages, villages_per_page)
    page_number = request.GET.get('page')

    try:
        current_page = paginator.get_page(page_number)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        #'matching_files': get_matching_files(request),
        'villages': current_page,
        'page_size': villages_per_page,
    }
    '''row_obj = Village.objects.filter(username=form.cleaned_data['username']).first()
    request.session["UserInfo"] = {
        'id': row_obj.id,
        'username': row_obj.username
    }'''
    return render(request, 'show.html', context)

def index(request, pk):
    #pattern = re.compile(str(request.session['UserInfo'].get("id")) + r'.*')
    #matching_files = find_image(request)
    # 查询并返回数据
    query_set = Village.objects.filter(id=pk)
    # 获取用户数据
    obj = query_set.first()
    tmp_id=request.session['UserInfo'].get("id")
    user = User.objects.get(id=tmp_id)
    is_in = obj.members.filter(id=tmp_id).exists()
    if(user.username==obj.admin.username) :
        identity=1
    else: identity=0
    village_info = {
        "id": pk,
        "villagename": obj.villagename,
        #"mobile_phone": obj.mobile_phone,
        #"gender": obj.get_gender_display(),
        "admin": obj.admin,
        "adminemail": obj.adminemail,
        "maxim":obj.maxim,
        "ingroup":is_in,
        "members":obj.members,   #use this to get group members
        'identity': identity
    }
    request.session["GroupInfo"] = {
        'id': obj.pk,
        'username': obj.villagename
    }
    return render(request, "index.html", context=village_info)

def showapplications(request,pk):
    gid=pk
    print(pk)
    village=Village.objects.get(id=pk)
    applications=village.applicants.all()
    context={
        'applications': applications,
        'group_id':gid,
    }
    return render(request, 'applications.html', context)





def show(request):
    
    villages = Village.objects.order_by('villagename')  #这里看看要不要根据群组人数什么的进行排序

    villages_per_page = 20
    paginator = Paginator(villages, villages_per_page)
    page_number = request.GET.get('page')

    try:
        current_page = paginator.get_page(page_number)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        #'matching_files': get_matching_files(request),
        'villages': current_page,
        'page_size': villages_per_page,
    }
    '''row_obj = Village.objects.filter(username=form.cleaned_data['username']).first()
    request.session["UserInfo"] = {
        'id': row_obj.id,
        'username': row_obj.username
    }'''
    return render(request, 'show.html', context)

def manage(request,gid,theapplicant):
    village=Village.objects.get(id=gid)
    theapplicant=User.objects.get(username=theapplicant)
    village.members.add(theapplicant)
    Experience.objects.create(experience=0, admin=village, user=theapplicant )  
    gid=village.id
    context = {
        'gid':gid
    }
    apply_instance = get_object_or_404(Application, applicant=theapplicant,goal=village)  
    apply_instance.delete()      
    return render(request, 'addmember.html',context)


def delete(request,name,applicant):
    village=Village.objects.get(villagename=name)
    theapplicant=User.objects.get(username=applicant)
    gid=village.id
    village.members.remove(theapplicant)
    context = {
        'gid':gid
    }  
    return render(request, 'delete.html',context)

def my_ajax_view(request):  
    if request.method == 'POST':  
        try:  
            data = json.loads(request.body)  
            param1 = data.get('param1')  
            param2 = data.get('param2')  
            # 执行一些逻辑  
            result = {'status': 'success', 'param1': param1, 'param2': param2}  
            return JsonResponse(result)  
        except json.JSONDecodeError:  
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)  
    else:  
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
