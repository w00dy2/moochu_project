from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . import models, forms
from django.contrib import messages
import logging

############## Post 관련 ##############

logger=logging.getLogger('board')

def moobo(request):
    post_list = models.board.objects.order_by('-create_date')
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='main'
    logger.info(f'board,{info_string}', extra={'user_id': user_id})
    return render(request, 'board/moobo.html', {'post_list': post_list})


def detail(request, post_id):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='board'
    logger.info(f'board_detail,{info_string}', extra={'user_id': user_id})
    post = get_object_or_404(models.board, pk=post_id)
    voted = post.voter.filter(id=request.user.id).exists()
    is_writer = request.user == post.writer
    
    response = render(request, 'board/post_detail.html', {'post': post, 'voted': voted, 'is_writer': is_writer})
    
    if not request.COOKIES.get(f'post_{post_id}_viewed'):  # 쿠키 확인
        post.update_counter()  # 조회수 증가
        response.set_cookie(f'post_{post_id}_viewed', 'true')  # 쿠키 설정
    
    return response


@login_required
def post(request):
    if request.method == "POST":
        form = forms.post_form(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            board.writer = request.user
            board.save()
            if request.user.is_authenticated:
                user_id = request.user.id
            else:
                user_id = None
            info_string='board'
            logger.info(f'post,{info_string}', extra={'user_id': user_id})
            return redirect('board:moobo')
    else:
        form = forms.post_form()

    context = {'form': form}
    return render(request, 'board/post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='post_edit'
    logger.info(f'board,{info_string}', extra={'user_id': user_id})
    if request.user != post.writer:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:post_detail', post_id=post.id)

    if request.method == "POST":
        form = forms.post_form(request.POST, instance=post)
        if form.is_valid():
            board = form.save(commit=False)
            board.writer = request.user
            board.modify_date = timezone.now()  # 수정일시 저장
            board.save()
            return redirect('board:post_detail', post_id=post.id)
    else:
        form = forms.post_form(instance=post)
    
    context = {'form': form}
    return render(request, 'board/post.html', context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    if request.user != post.writer:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', post_id=post.id)
    post.delete()
    return redirect('board:moobo')



############## Comment 관련 ##############

def comment(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='comment_detail'
    logger.info(f'board,{info_string}', extra={'user_id': user_id})
    post.comment_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('board:detail', post_id = post.id)


@login_required
def comment_create(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='comment_create'
    logger.info(f'board,{info_string}', extra={'user_id': user_id})
    if request.method == "POST":
        form = forms.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = request.user
            comment.create_date = timezone.now()
            comment.board = post
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('board:post_detail', post_id=comment.board.id), comment.id))
    else:
        form = forms.comment_form()
    context = {'form': form}
    return render(request, 'board/comment_create.html', context)



@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(models.comment, pk=comment_id)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='comment_edit'
    logger.info(f'board,{info_string}', extra={'user_id': user_id})
    if request.user != comment.writer:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:post_detail', post_id=comment.board.id)

    if request.method == "POST":
        form = forms.comment_form(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('board:post_detail', post_id=comment.board.id)
    else:
        form = forms.comment_form(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'board/comment_create.html', context)


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(models.comment, pk=comment_id)
    if request.user != comment.writer:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('board:post_detail', post_id=comment.board.id)


############## 추천 관련 ##############

@login_required
def vote_post(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    if request.user == post.writer:
        pass # 오류메세지는 js로 작성 post_detail.html 맨 아래쪽 script 코드 참조
    elif post.voter.filter(id=request.user.id).exists():
        pass # 오류메세지는 js로 작성 post_detail.html 맨 아래쪽 script 코드 참조
    else:
        post.voter.add(request.user)
    
    return redirect('board:post_detail', post_id=post.id)


@login_required
def vote_comment(request, comment_id):
    comment = get_object_or_404(comment, pk=comment_id)
    if request.user == comment.writer:
        pass # 오류메세지는 js로 작성 post_detail.html 맨 아래쪽 script 코드 참조
    elif comment.voter.filter(id=request.user.id).exits():
        pass # 오류메세지는 js로 작성 post_detail.html 맨 아래쪽 script 코드 참조
    else:
        comment.voter.add(request.user)
    return redirect('board:post_detail', post_id=comment.board.id)




############## My Posts ##############
@login_required
def my_posts(request, user_id):
    writer = models.User.objects.get(pk=user_id)
    post_list = models.board.objects.filter(writer=writer).order_by('-create_date')
    context = {
        'post_list': post_list,
    }
    return render(request, 'board/moobo.html', context)