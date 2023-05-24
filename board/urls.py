from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="posts"),
    path('create/', views.PostCreate.as_view(), name="add_post"),
    path('<int:pk>/', views.PostDetail.as_view(), name="post_d"),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name="update_post"),
    path('<int:pk>/respond/', views.ReplyCreate.as_view(), name="reply_edit"),
    path('reply/', views.ReplyList.as_view(), name="reply_list"),
    path('reply/<int:pk>/', views.ReplyDetail.as_view(), name="reply_d"),
    path('reply/<int:pk>/accept/', views.accept_reply, name="accept"),
    path('reply/<int:pk>/deny/', views.deny_reply, name="deny"),
    path('success/', views.SuccessView.as_view(), name="success"),
]