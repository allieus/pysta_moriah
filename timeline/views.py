# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.paginator import Paginator

from utils import utils
from .models import Post, Comment
from .forms import PostingForm, CommentForm

# 좋아요
def like(request, post_id):

    # post 찾기
    p = Post.objects.get(id=post_id)
    
    # 좋아요 한 사용자 추가하기
    p.liked.add(request.user)
    
    # profile page 로 redirect
    return redirect(request.GET["next"])

    
# 좋아요 취소
def unlike(request, post_id):

    # post 찾기
    p = Post.objects.get(id=post_id)
    
    # 좋아요 한 사용자 삭제하기
    p.liked.remove(request.user)
    
    # profile page 로 redirect
    return redirect(request.GET["next"])


# 댓글 쓰기
def do_comment(request, post_id):
    # 폼 제출시
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)

            # post 찾기
            post = Post.objects.get(id=post_id)

            # owner/부모 post 설정 및 저장
            comment.owner = request.user
            comment.post = post
            comment.save()
            
        return redirect(request.POST["next"])
    else:
        # 잘못된 접근. todo: 에러 처리
        pass

        
# 코멘트 삭제
def remove_comment(request, comment_id):

    # comment 찾기
    c = Comment.objects.get(id=comment_id)
    
    if (c.owner == request.user):
        c.delete()
    
    # profile page 로 redirect
    return redirect(request.GET["next"])

    
# profile, 글 리스트 보기
class ProfileView(ListView):
    model = Post
    template_name = "timeline/profile.html"
    context_object_name = "posts"
    paginate_by = 1
    
    # 대상 Queryset 설정
    def get_queryset(self):
        
        # parameter 로 가져올 페이지 주인 찾기
        
        # 파라미터 지정시 => 지정된 사용자
        if self.kwargs.has_key("user_id"):
            uid = self.kwargs['user_id']
            self.page_owner = get_user_model().objects.get(id=uid)
        
        # 파라미터 미 지정시 => 로그인 사용자
        else:
            uid = self.request.user.id
            self.page_owner = self.request.user
        
        # QuerySet 설정하고 리턴
        qs = super(ProfileView, self).get_queryset()
        qs = qs.filter(owner_id=self.page_owner.id).order_by('-id')
        return qs;
    
    # context 추가
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['page_owner'] = self.page_owner
        context['form'] = PostingForm()
        if self.kwargs.has_key("page"):
            context['page'] = self.kwargs['page']
        else:
            context['page'] = 1
            
        context['comment_form'] = CommentForm()
        return context

profile = ProfileView.as_view()


# 글 쓰기 처리
def post(request):
    # 폼 제출시
    if request.method == 'POST':
        form = PostingForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            
            # 이미지 업로드
            filename = ""
            if (request.FILES.has_key("photo")):
                filename = utils.upload(request.FILES["photo"], "post")
                utils.make_thumb(filename, "post", 600, 900)
                post.image = filename
            
            # owner 설정 및 저장
            post.owner = request.user
            post.save()
            
            return redirect('profile:profile')
    else:
        # 잘못된 접근. todo: 에러 처리
        pass
        