from django.views import generic
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from .models import Post, Reply, User
from .forms import PostForm, ReplyForm

class PostList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post_d.html'
    context_object_name = 'post_d'

class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'add_post'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        return result

class PostUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    context_object_name = 'update_post'

    def get_template_names(self):
        post = self.get_object()
        if post.user == self.request.user:
            self.template_name = 'post_edit.html'
            return self.template_name
        else:
            raise PermissionDenied

class ReplyList(ListView, LoginRequiredMixin):
    model = Reply
    ordering = '-reply_time'
    template_name = 'reply_list.html'
    context_object_name = 'reply_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Reply.objects.filter(post__user=self.request.user)
        return queryset

class ReplyDetail(DetailView):
    model = Reply
    context_object_name = 'reply_d'
    def get_template_names(self):
        reply = self.get_object()
        if reply.post.user == self.request.user:
            self.template_name = 'reply_d.html'
            return self.template_name
        else:
            raise PermissionDenied

class ReplyCreate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'
    context_object_name = 'reply_edit'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.post = Post.objects.get(id=self.kwargs['pk'])
        self.object.save()
        result = super().form_valid(form)
        send_mail(
            subject=f'Получен отклик на пост "{self.object.post.title}"',
            message=f'Отклик: "{self.object.body}"',
            from_email='news-mews-sergeeva@yandex.ru',
            recipient_list=[self.object.post.user.email]
        )
        return result
class SuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'success.html'

@login_required()
def accept_reply(request, pk):
    reply = Reply.objects.get(pk=pk)
    reply.status = 'A'
    reply.save()
    send_mail(
        subject=f'Доска объявлений: отлик принят',
        message=f'Ваш отклик на пост "{reply.post.title}" принят',
        from_email='news-mews-sergeeva@yandex.ru',
        recipient_list=[reply.user.email]
    )
    return HttpResponseRedirect(reverse('reply_list'))


@login_required()
def deny_reply(request, pk):
    reply = Reply.objects.get(pk=pk)
    reply.status = 'D'
    reply.save()
    return HttpResponseRedirect(reverse('reply_list'))



