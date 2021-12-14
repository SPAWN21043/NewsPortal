from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.shortcuts import render
from .filters import SearchFilter, AddFilter
from django.core.paginator import Paginator
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = "posts"

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class AddList(CreateView):
    template_name = 'add.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

