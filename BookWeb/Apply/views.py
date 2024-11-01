from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from Apply.Forms import CreateForm
from UserAuth.models import User
from django.shortcuts import render, HttpResponse, redirect
from Groups.models import Village;
from django.core.paginator import Paginator, EmptyPage
import re
# Create your views here.

def create(request):
    if request.method=='GET':
        form = CreateForm(request=request)
        context = {
            'form': form,
            'nid': 1  # represent registration
        }
        return render(request, 'apply.html', context=context)
    form = CreateForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
            'nid': 1
        }
        return render(request, 'apply.html', context=context)
    tmp_id=request.session['GroupInfo'].get("id")
    if tmp_id==None:
        return redirect("/info/info/")
    group = Village.objects.get(id=tmp_id)
    #form.admin_id= request.session['UserInfo'].get("id")
    form.instance.goal=group
    form.save()
    return redirect("/")