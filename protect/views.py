
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import ReplyFilter
from board.models import Reply, Post, SubscribedUsers


class IndexView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'protect/index.html'
    context_object_name = 'reply_list'
    ordering = '-date'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ReplyFilter(self.request.GET, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_list'] = Reply.objects.filter(user=self.request.user.id).order_by('-date')
        context['is_not_subscribed'] = False if SubscribedUsers.objects.filter(user=self.request.user.id).exists() else True
        return context

class ReplyByPost(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'protect/reply_by_post.html'
    ordering = '-date'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reply_list_by_postid = Reply.objects.filter(post=self.kwargs['pk']).order_by('-date')
        post = Post.objects.get(id=self.kwargs['pk'])
        context['reply_list'] = reply_list_by_postid
        context['post'] = post
        return context

@login_required
def accept_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    if reply:
        reply.accepted = True
        reply.save(update_fields=['accepted'])

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_reply(request, pk):
    Reply.objects.get(id=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def subscribe(request):
    subscribe = SubscribedUsers()
    subscribe.user = request.user
    subscribe.save()
    return redirect(request.META.get('HTTP_REFERER'))
