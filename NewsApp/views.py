from django import views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Article
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


class BaseListView(ListView):
    template_name = 'NewsApp/home.html'
    queryset = Article.objects.order_by('-date')


def about(request):
    return render(request, 'NewsApp/about.html')


class ArticleListView(ListView):
    queryset = Article.objects.all().order_by('-date')
    template_name = 'NewsApp/home.html'


    def get_context_data(self, object_list=None, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'NewsApp/news_detail.html'

    # def get_queryset(self, **kwargs):
    #     queryset = Article.objects.filter(category__slug=self.kwargs['slug'], status='published').order_by('-date')
    #     return queryset


class CategoryDetail(ListView):
    template_name = 'NewsApp/category_detail.html'
    paginate_by = 8

    def get_queryset(self, **kwargs):
        queryset = Article.objects.filter(category__slug=self.kwargs['slug'], status='published').order_by('-date')
        return queryset


class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'NewsApp/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'NewsApp/registration.html', context)


class RegistrationView(views.View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'NewsApp/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'NewsApp/registration.html', context)