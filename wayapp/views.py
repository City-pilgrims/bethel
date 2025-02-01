from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from wayapp.decorators import pilgrim_ownership_required
from wayapp.forms import NoteCreateForm, NoteUpdateForm, PhotoUpdateFormSet
from wayapp.models import Note, Photo


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteCreateForm
    template_name = "wayapp/crispy_form.html"
    extra_context = {"form_title": "매일순례"}

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

class NoteDetailView(DetailView):
    model = Note
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
