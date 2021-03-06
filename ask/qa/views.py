# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from qa.models import *
from qa.forms import *


def paginate(request, qs):

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
        
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1 #raise Http404
        
    #limit = 10
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
        
    return page



@require_GET
def test(request, *args, **kwargs):
    return HttpResponse('OK')



def question_details(request, id):
    #if request.method == "POST": 
        #return add_answer(request)
    
    question = get_object_or_404(Question, id=int(id))
        
    if request.method == "POST":
        form = AnswerForm(request.POST, _question=question)
        form._user = request.user
        if form.is_valid():
            answer = form.save()
            url = answer.question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question' : question.id})
        
    return render(request, 'question_details.html', {
        'question': question,
        'answers': question.answer_set.all(),
        'form': form,
        #'POST_url': request.path,
        'webpage_title': 'Question details',
    })



@require_GET
def questions(request):
    page = paginate(request, Question.objects.order_by('-id'))
    return render(request, 'questions.html', {
        'page': page,
        'baseurl': '/?page=',
        'webpage_title': 'New questions',
    })
    
    

@require_GET    
def popular_questions(request):
    page = paginate(request, Question.objects.order_by('-rating'))
    return render(request, 'questions.html', {
        'page': page,
        'baseurl': '/popular/?page=',
        'webpage_title': 'Popular questions',
    })    



def new_question(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            #return HttpResponse(str(form.cleaned_data))
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'new_question.html', {
        'form': form,
        'webpage_title': 'New question',
    })



@require_POST
def add_answer(request): #stub for test
    return HttpResponse('OK')
    #return HttpResponse(str(request.POST.get('question', 'X')))



def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            #return HttpResponse('OK '+str(form.cleaned_data))
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'form.html', {
        'form': form,
        'POST_url': '/signup/',
        'webpage_title': 'Создание нового пользователя',
    })



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'form.html', {
        'form': form,
        'POST_url': '/login/',
        'webpage_title': 'Авторизация',
    })








