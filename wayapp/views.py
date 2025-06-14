from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from commentapp.forms import CommentCreationForm
from wayapp.forms import NoteCreateForm, NoteUpdateForm, PhotoUpdateFormSet, VideoForm
from wayapp.models import Note, Photo, SpecialPilgrim, PilgrimImage, PilgrimDescription, PilgrimVideo


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteCreateForm
    template_name = "wayapp/crispy_form.html"
    extra_context = {"form_title": "매일순례"}

    def dispatch(self, request, *args, **kwargs):
        if not (
                request.user.groups.filter(name="Toledot").exists() or
                request.user.groups.filter(name="Commander").exists()
        ):
            messages.error(request, "순례자들교회 등록 지체들만 작성가능합니다.")
            return redirect("wayapp:list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)  # noqa

        new_note = self.object
        new_note.author = self.request.user
        new_note.save()

        photo_file_list = form.cleaned_data.get("photos")
        if photo_file_list:
            Photo.create_photos(new_note, photo_file_list)

        messages.success(self.request, "새 기록을 저장했습니다.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wayapp:detail', kwargs={'pk': self.object.pk})


@login_required
def NoteUpdateView(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    photo_qs = note.photo_set.all()

    if request.method == "GET":
        note_form = NoteUpdateForm(instance=note, prefix="note")
        photo_formset = PhotoUpdateFormSet(
            queryset=photo_qs,
            instance=note,
            prefix="photos",
        )
    else:
        note_form = NoteUpdateForm(
            data=request.POST, files=request.FILES, instance=note, prefix="note"
        )
        photo_formset = PhotoUpdateFormSet(
            queryset=photo_qs,
            instance=note,
            data=request.POST,
            files=request.FILES,
            prefix="photos",
        )

        if note_form.is_valid() and photo_formset.is_valid():
            saved_note = note_form.save()

            photo_file_list = note_form.cleaned_data.get("photos")
            if photo_file_list:
                Photo.create_photos(saved_note, photo_file_list)

            photo_formset.save()
            messages.success(request, f"기록#{saved_note.pk}을 수정했습니다.")

            return redirect(saved_note)

    return render(
        request,
        "wayapp/crispy_form_and_formset.html",
        {
            "form_title": "매일순례 업데이트",
            "form": note_form,
            "formset": photo_formset,
            "form_submit_label": "저장하기",
        },
    )


class NoteDetailView(DetailView, FormMixin):
    model = Note
    form_class = CommentCreationForm
    template_name = 'wayapp/detail.html'


class NoteListView(ListView):
    model = Note
    context_object_name = 'note_list'
    template_name = 'wayapp/list.html'


@login_required
def NoteDeleteView(request, pk):
    # 대상 컨텐츠 가져 오기
    note = get_object_or_404(Note, pk=pk)

    # 삭제실행
    note.delete()

    return redirect(reverse('wayapp:list'))


@login_required
def like_note(request, pk):
    """좋아요 기능"""
    note = get_object_or_404(Note, pk=pk)

    if request.user in note.likes.all():
        note.likes.remove(request.user)  # 좋아요 취소
    else:
        note.likes.add(request.user)  # 좋아요 추가

    return HttpResponseRedirect(reverse("wayapp:detail", kwargs={"pk": pk}))


@login_required
def SPindex(request):
    return render(request, 'wayapp/spadd.html')


@login_required
def SPadd_item(request):
    if not (
            request.user.groups.filter(name='Toledot').exists() or
            request.user.groups.filter(name='Commander').exists()
    ):
        messages.error(request, "순례자들교회 등록 지체들만 작성가능합니다.")
        return redirect("wayapp:splist")
        #return JsonResponse({'error': 'Toledot 그룹만 작성할 수 있습니다.'}, status=403)

    if request.method == "POST":
        author = request.user
        selected_pil_group = request.POST.get('pil_group')
        custom_pil_group = request.POST.get('pil_group_custom')

        if selected_pil_group == "custom_group" and custom_pil_group:
            pil_group_name = custom_pil_group

        elif selected_pil_group == "#":
            pil_group_name = "특별"

        else:
            pil_group_name = selected_pil_group

        # 새로운 SpecialPilgrim 객체 생성
        special_pilgrim = SpecialPilgrim.objects.create(author=author, group=pil_group_name)

        images = request.FILES.getlist('images')
        descriptions = request.POST.getlist('descriptions')

        if len(images) != len(descriptions):  # 사진과 설명 개수 맞추기
            return JsonResponse({'error': '이미지와 설명의 개수가 일치하지 않습니다.'}, status=400)

        for image in images:
            PilgrimImage.objects.create(special_pilgrim=special_pilgrim, image=image)

        for description in descriptions:
            PilgrimDescription.objects.create(special_pilgrim=special_pilgrim, text=description)

        return JsonResponse({'success': True, 'content_id': special_pilgrim.id})

        return JsonResponse({'error': '잘못된 요청'}, status=400)


@login_required
def SPupdate_item(request, pk):
    special_pilgrim = get_object_or_404(SpecialPilgrim, id=pk, author=request.user)  # 본인만 수정 가능

    if request.method == "GET":
        images = PilgrimImage.objects.filter(special_pilgrim=special_pilgrim)
        descriptions = PilgrimDescription.objects.filter(special_pilgrim=special_pilgrim)
        image_description_pairs = list(zip(images, descriptions))  # zip()을 리스트로 변환

        return render(request, 'wayapp/spupdate.html', {
            'special_pilgrim': special_pilgrim,
            'image_description_pairs': image_description_pairs
        })

    elif request.method == "POST":
        selected_pil_group = request.POST.get('pil_group')
        custom_pil_group = request.POST.get('pil_group_custom')

        if selected_pil_group == "custom_group" and custom_pil_group:
            special_pilgrim.group = custom_pil_group
        elif selected_pil_group == "#":
            special_pilgrim.group = "특별"
        else:
            special_pilgrim.group = selected_pil_group

        special_pilgrim.save()

        # 기존 데이터 유지하면서 업데이트하기
        description_ids = request.POST.getlist('description_ids')
        existing_descriptions = request.POST.getlist('existing_descriptions')
        new_images = request.FILES.getlist('new_images')
        new_descriptions = request.POST.getlist('new_descriptions')

        # 기존 설명 업데이트
        for desc_id, new_text in zip(description_ids, existing_descriptions):
            description = get_object_or_404(PilgrimDescription, id=desc_id, special_pilgrim=special_pilgrim)
            description.text = new_text
            description.save()

        # 새 이미지와 설명 추가
        for image, description in zip(new_images, new_descriptions):
            PilgrimImage.objects.create(special_pilgrim=special_pilgrim, image=image)
            PilgrimDescription.objects.create(special_pilgrim=special_pilgrim, text=description)

        return JsonResponse({'success': True, 'content_id': special_pilgrim.pk})

    return JsonResponse({'error': '잘못된 요청'}, status=400)


def SPlist(request):
    special_pilgrims = SpecialPilgrim.objects.all().order_by('-id')

    # 각 SpecialPilgrim에 대한 대표 이미지 가져오기
    special_pilgrim_list = []
    for special_pilgrim in special_pilgrims:
        representative_image = PilgrimImage.objects.filter(special_pilgrim=special_pilgrim).first()
        special_pilgrim_list.append({
            'pilgrim': special_pilgrim,
            'image': representative_image.image.url if representative_image else None
        })

    return render(request, 'wayapp/splist.html', {'pilgrim_list': special_pilgrim_list})


def SPdetail(request, pk):
    special_pilgrim = get_object_or_404(SpecialPilgrim, id=pk)

    # ForeignKey 관계로 연결된 이미지와 설명 가져오기
    images = PilgrimImage.objects.filter(special_pilgrim=special_pilgrim)
    descriptions = PilgrimDescription.objects.filter(special_pilgrim=special_pilgrim)

    # 이미지와 설명 쌍 생성
    image_description_pairs = list(zip(images, descriptions))

    return render(request, 'wayapp/spdetail.html', {
        'special_pilgrim': special_pilgrim,
        'image_description_pairs': image_description_pairs
    })


@login_required
def SPdelete(request, pk):
    # 대상 컨텐츠 가져 오기
    special_pilgrim = get_object_or_404(SpecialPilgrim, id=pk)

    # 삭제실행
    special_pilgrim.delete()

    return redirect(reverse('wayapp:splist'))


@login_required
def PILvideo_upload(request):
    if not (
            request.user.groups.filter(name='Toledot').exists() or
            request.user.groups.filter(name='Commander').exists()
    ):
        messages.error(request, "순례자들교회 등록 지체들만 작성가능합니다.")
        return redirect('wayapp:pilvideolist')

    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)  # 임시 저장
            video.author = request.user  # 현재 로그인한 사용자를 author로 설정
            video.save()
            return redirect('wayapp:pilvideolist')  # 업로드 후 리스트 페이지로 이동
    else:
        form = VideoForm()
    return render(request, 'wayapp/video_upload.html', {'form': form})


def PILvideo_list(request):
    videos = PilgrimVideo.objects.all().order_by('-uploaded_at')  # 최신순 정렬
    return render(request, 'wayapp/video_list.html', {'videos': videos})


@login_required
def PILvideo_delete(request, pk):

    if request.method == "POST":
        video = get_object_or_404(PilgrimVideo, pk=pk, author=request.user)
        video.delete()
        return redirect('wayapp:pilvideolist')

    return redirect('wayapp:pilvideolist')