from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list,name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/',views.post_edit,name='post_edit'),
    path('draft/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/',views.post_publish, name='post_publish'),
    path('post/<pk>/delete/',views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    path('comment/<int:pk>/approve/', views.approve_comment, name='approve_comment'),
    path('accounts/register/',views.register, name='register'),
    path('profile/',views.profile,name='profile'),
    path('bloggers/',views.blogger_list,name='blogger_list'),
    path('blogger/<int:pk>/',views.blogger_detail,name='blogger_detail')
]