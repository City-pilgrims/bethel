from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings

# Create your views here.
from pilgrimsapp.forms import PilgrimBoardForm
from pilgrimsapp.models import TimelineEvent, PilgrimBoard


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



