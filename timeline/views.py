# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
        
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


# follower, follower list
class FollowerView(ListView):
    
    template_name = "timeline/followers.html"
    
    # 대상 Queryset 설정
    def get_queryset(self):
        
        # parameter 로 가져올 페이지 주인 찾기
        uid = self.kwargs['user_id']
        self.page_owner = get_user_model().objects.get(id=uid)
        
        qs = self.page_owner.profile.follower.all()
        return qs;
    
    # context 추가
    def get_context_data(self, **kwargs):
        context = super(FollowerView, self).get_context_data(**kwargs)
        context['page_owner'] = self.page_owner
        return context
        
followers = FollowerView.as_view()

# following list
class FollowingView(ListView):
    template_name = "timeline/followings.html"
    
    # 대상 Queryset 설정
    def get_queryset(self):
        
        # parameter 로 가져올 페이지 주인 찾기
        uid = self.kwargs['user_id']
        self.page_owner = get_user_model().objects.get(id=uid)
        
        qs = self.page_owner.profile.following.all()
        return qs;
    
    # context 추가
    def get_context_data(self, **kwargs):
        context = super(FollowingView, self).get_context_data(**kwargs)
        context['page_owner'] = self.page_owner
        return context
        
followings = FollowingView.as_view()

# timeline
class TimelinePullView(ListView):
    model = Post
    template_name = "timeline/timeline.html"
    context_object_name = "posts"
    
    # 대상 Queryset 설정
    def get_queryset(self):
        # QuerySet 설정하고 리턴
        qs = super(TimelineView, self).get_queryset()
        
        # step 1. 내가 following 하는 사람들 profile 가져오기
        profiles_i_follow = self.request.user.profile.following.all()
        
        # step 2. 해당 profile 의 user 목록 가져오기
        follow_users = get_user_model().objects.filter(profile__in=profiles_i_follow)
        
        # step 3. 해당 user 들이 쓴 글 가져오기
        q1 = Q(owner__in=follow_users)
        
        # step 4. 내가 쓴 글 가져오기
        q2 = Q(owner=self.request.user)
        
        # 원하는 결과: step 3 + step 4
        qs = qs.filter(q1 | q2).order_by('-id')
        
        return qs;
    
    # context 추가
    def get_context_data(self, **kwargs):
        context = super(TimelinePullView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
        
timeline_pull = TimelinePullView.as_view()

# timeline
class TimelineView(ListView):
    model = Post
    template_name = "timeline/timeline.html"
    context_object_name = "posts"
    
    # 대상 Queryset 설정
    def get_queryset(self):
        # QuerySet 설정하고 리턴
        qs = self.request.user.profile.timeline.order_by('-id')

        return qs;
    
    # context 추가
    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
        
timeline = TimelineView.as_view()


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
            
            # post 배송하기 (push timeline)
            for follower in request.user.profile.follower.all():
                # 친구에게 배송하기
                post.reader.add(follower)
            
            # 나에게도 배송하기
            post.reader.add(request.user.profile)
            
            return redirect('profile:profile')
    else:
        # 잘못된 접근. todo: 에러 처리
        pass

        
# 친구 맺기
def follow(request, user_id):

    # 친구 찾기
    u = get_user_model().objects.get(id=user_id)
    
    # 친구의 follower 로 나를 추가하기
    u.profile.follower.add(request.user.profile)
    
    # 지금까지 쓴 글 배송하기
    for post in u.posts.all():
        request.user.profile.timeline.add(post)
    
    # redirect
    return redirect(request.META['HTTP_REFERER'])
    

# 친구 제거
def unfollow(request, user_id):

    # 친구 찾기
    u = get_user_model().objects.get(id=user_id)
    
    # 친구의 follower 에서 나를 제거하기
    u.profile.follower.remove(request.user.profile)
    
    # 지금까지 배송된 글 제거하기
    # 제거할 대상 찾기
    posts_received = request.user.profile.timeline.filter(owner=u)
    # 제거하기
    request.user.profile.timeline.remove(*posts_received)
    
    # redirect
    return redirect(request.META['HTTP_REFERER'])

    