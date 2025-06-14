from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings

# Create your views here.
from pilgrimsapp.forms import PilgrimBoardForm, AnswerForm, SecretPasswordForm, QuestionForm
from pilgrimsapp.models import TimelineEvent, PilgrimBoard, Question, Answer


def intro_images(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], "intro_img")
    img_folder = os.path.join(settings.STATICFILES_DIRS[0], "intro_img")  # html 폴더 경로
    img_list = [f"intro_img/{img}" for img in os.listdir(img_folder) if img.endswith(('.png', '.jpg', '.jpeg', '.gif','.JPG','.PNG','.JPEG','.GIF'))]  # 이미지 파일만 필터링

    return render(request, "pilgrimsapp/intro.html", {"image_list": img_list})


def timeline_view(request):
    events = TimelineEvent.objects.all().order_by('-event_date')  # '-event_date'는 내림차순 정렬
    event_list = []

    # 이미지 URL을 완전한 URL로 변환
    for event in events:
        event_dict = {
            'event_date': event.event_date,
            'title': event.title,
            'description': event.description,
            'image_url': event.image.url if event.image else None,  # 이미지가 있으면 URL 반환
        }
        event_list.append(event_dict)

    return JsonResponse({'events': event_list})


def PilgrimBoardList(request):
    pilboard = PilgrimBoard.objects.all().order_by('-created_at')
    return render(request, 'pilgrimsapp/pilboard_list.html',{'pilboards': pilboard})


@login_required
def PilgrimBoardCreate(request):
    if request.method == 'POST':
        form = PilgrimBoardForm(request.POST, request.FILES)
        if form.is_valid():
            pilboard = form.save(commit=False)
            pilboard.author = request.user
            pilboard.save()
            return redirect('pilgrimsapp:pilboardlist')
    else:
        form = PilgrimBoardForm()

    return render(request, 'pilgrimsapp/pilboard_create.html', {'form': form})


@login_required
def PilgrimBoardUpdate(request, pk):
    pilboard = get_object_or_404(PilgrimBoard, pk=pk)

    # 작성자만 수정 가능하도록 확인
    if pilboard.author != request.user:
        return redirect('pilgrimsapp:pilboardlist')

    if request.method == 'POST':
        form = PilgrimBoardForm(request.POST, request.FILES, instance=pilboard)
        if form.is_valid():
            form.save()
            return redirect('pilgrimsapp:pilboarddetail', pk=pilboard.pk)
    else:
        form = PilgrimBoardForm(instance=pilboard)

    return render(request, 'pilgrimsapp/pilboard_update.html', {'form': form})



def PilgrimBoardDetail(request, pk):

    pilboard = get_object_or_404(PilgrimBoard, pk=pk)

    return render(request, 'pilgrimsapp/pilboard_detail.html', {'pilboard': pilboard})


@login_required
def PilgrimBoardDelete(request, pk):

    pilboard = get_object_or_404(PilgrimBoard, pk=pk)
    pilboard.delete()

    return redirect('pilgrimsapp:pilboardlist')


def question_list(request):
    """질문 목록"""
    questions = Question.objects.all()

    # 검색 기능
    search_query = request.GET.get('search')
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # 카테고리 필터
    category = request.GET.get('category')
    if category:
        questions = questions.filter(category=category)

    # 답변 상태 필터
    status = request.GET.get('status')
    if status == 'answered':
        questions = questions.filter(is_answered=True)
    elif status == 'unanswered':
        questions = questions.filter(is_answered=False)

    # 페이지네이션
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'status': status,
        'categories': Question.CATEGORY_CHOICES,
    }
    return render(request, 'pilgrimsapp/question_list.html', context)


def question_detail(request, pk):
    """질문 상세"""
    question = get_object_or_404(Question, pk=pk)

    # 비밀글 체크
    if question.is_secret:
        # 작성자 본인이 아닌 경우
        if not request.user.is_authenticated or request.user != question.author:
            # 관리자가 아닌 경우 비밀번호 확인
            if not request.user.is_staff:
                # 세션에서 비밀번호 확인 여부 체크
                session_key = f'secret_question_{pk}'
                if not request.session.get(session_key):
                    return redirect('pilgrimsapp:secret_check', pk=pk)

    # 조회수 증가 (작성자 본인 제외)
    if request.user != question.author:
        question.increment_views()

    # 답변 폼
    answer_form = AnswerForm()

    context = {
        'question': question,
        'answer_form': answer_form,
    }
    return render(request, 'pilgrimsapp/question_detail.html', context)


def secret_check(request, pk):
    """비밀글 비밀번호 확인"""
    question = get_object_or_404(Question, pk=pk)

    if not question.is_secret:
        return redirect('pilgrimsapp:detail', pk=pk)

    if request.method == 'POST':
        form = SecretPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if password == question.password:
                # 세션에 비밀번호 확인 상태 저장
                request.session[f'secret_question_{pk}'] = True
                return redirect('pilgrimsapp:detail', pk=pk)
            else:
                messages.error(request, '비밀번호가 올바르지 않습니다.')
    else:
        form = SecretPasswordForm()

    context = {
        'form': form,
        'question': question,
    }
    return render(request, 'pilgrimsapp/secret_check.html', context)


@login_required
def question_create(request):
    """질문 작성"""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            #messages.success(request, '질문이 등록되었습니다.')
            return redirect('pilgrimsapp:detail', pk=question.pk)
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pilgrimsapp/question_create.html', context)


@login_required
def question_update(request, pk):
    """질문 수정"""
    question = get_object_or_404(Question, pk=pk)

    # 작성자 본인만 수정 가능
    if request.user != question.author:
        messages.error(request, '본인이 작성한 질문만 수정할 수 있습니다.')
        return redirect('pilgrimsapp:detail', pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, '질문이 수정되었습니다.')
            return redirect('pilgrimsapp:detail', pk=pk)
    else:
        form = QuestionForm(instance=question)

    context = {
        'form': form,
        'question': question,
    }
    return render(request, 'pilgrimsapp/question_update.html', context)


@login_required
def question_delete(request, pk):
    """질문 삭제"""
    question = get_object_or_404(Question, pk=pk)

    # 작성자 본인 또는 관리자만 삭제 가능
    if request.user != question.author and not request.user.is_staff:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pilgrimsapp:detail', pk=pk)

    if request.method == 'POST':
        question.delete()
        messages.success(request, '질문이 삭제되었습니다.')
        return redirect('pilgrimsapp:list')

    context = {'question': question}
    return render(request, 'pilgrimsapp/question_delete.html', context)


@login_required
def answer_create(request, pk):
    """답변 작성"""
    question = get_object_or_404(Question, pk=pk)

    # ✅ 그룹 확인: 'Toledot'에 속한 사용자만 가능
    aa = request.user.groups.name
    print(aa)
    if not request.user.groups.filter(name='Commander').exists():
        messages.error(request, 'Toledot 그룹에 속한 사용자만 답변을 작성할 수 있습니다.')
        return redirect('pilgrimsapp:detail', pk=pk)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            # 관리자가 답변하는 경우 공식 답변으로 설정
            if request.user.is_staff:
                answer.is_official = True
            answer.save()
            messages.success(request, '답변이 등록되었습니다.')
            return redirect('pilgrimsapp:detail', pk=pk)

    return redirect('pilgrimsapp:detail', pk=pk)


@login_required
def answer_update(request, pk, answer_pk):
    """답변 수정"""
    question = get_object_or_404(Question, pk=pk)
    answer = get_object_or_404(Answer, pk=answer_pk, question=question)

    # 작성자 본인만 수정 가능
    if request.user != answer.author:
        messages.error(request, '본인이 작성한 답변만 수정할 수 있습니다.')
        return redirect('pilgrimsapp:detail', pk=pk)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, '답변이 수정되었습니다.')
            return redirect('pilgrimsapp:detail', pk=pk)
    else:
        form = AnswerForm(instance=answer)

    context = {
        'form': form,
        'question': question,
        'answer': answer,
    }
    return render(request, 'pilgrimsapp/answer_update.html', context)


@login_required
def answer_delete(request, pk, answer_pk):
    """답변 삭제"""
    question = get_object_or_404(Question, pk=pk)
    answer = get_object_or_404(Answer, pk=answer_pk, question=question)

    # 작성자 본인 또는 관리자만 삭제 가능
    if request.user != answer.author and not request.user.is_staff:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pilgrimsapp:detail', pk=pk)

    if request.method == 'POST':
        answer.delete()

        # 답변이 모두 삭제되면 질문의 답변 완료 상태 업데이트
        if not question.answers.exists():
            question.is_answered = False
            question.save(update_fields=['is_answered'])

        messages.success(request, '답변이 삭제되었습니다.')
        return redirect('pilgrimsapp:detail', pk=pk)

    context = {
        'question': question,
        'answer': answer,
    }
    return render(request, 'pilgrimsapp/answer_delete.html', context)
