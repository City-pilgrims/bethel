from os.path import splitext

from PIL import Image, ImageSequence
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from typing import List

from django.core.files import File
from django.core.files.base import ContentFile
from django.forms import BaseInlineFormSet, inlineformset_factory

from wayapp.models import Note, Photo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_clean = super().clean  # 함수를 호출하지 않습니다.
        if isinstance(data, (list, tuple)):
            return [single_clean(file) for file in data]
        else:
            return single_clean(data)


def make_thumb(
        image_file: File, max_width: int = 1024, max_height: int = 1024, quality=80
) -> File:
    pil_image = Image.open(image_file)
    max_size = (max_width, max_height)
    pil_image.thumbnail(max_size)
    img_format = pil_image.format

    if img_format == "GIF":
        image_data = image_file.read()
        #frames = [frame.copy() for frame in ImageSequence.Iterator(image_data)]
        thumb_file = ContentFile(image_data, name=image_file.name)
        pil_image.save(thumb_file)
        return thumb_file
    else:
        # 만약 이미지가 RGBA(알파 채널 포함) 모드라면 RGB 모드로 변환
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")

        thumb_name = splitext(image_file.name)[0] + ".jpg" # Splittext(os.path)는 파일 이름에서 확장자를 분리하는데 활용

        # 썸네일 파일 생성: 비어있는 ContentFile 객체 생성 후 이름 설정, ContentFile(django.core.files.base.ContentFile)은 파일 이름을 받아 파일 객체처럼 사용
        thumb_file = ContentFile(b"", name=thumb_name)

        # PIL을 사용하여 이미지를 JPEG 형식으로 저장하고 지정된 품질로 설정
        pil_image.save(thumb_file, format="jpeg", quality=quality)

        return thumb_file


class NoteCreateForm(forms.ModelForm):
    photos = MultipleImageField(required=True)

    class Meta:
        model = Note
        fields = ["title", "content", "tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": True}
        self.helper.form_class = "helper_form"
        self.helper.label_class = "helper_label"

        self.helper.layout = Layout("title", "content", "photos", "tags")
        self.helper.add_input(
            Submit(
                "submit",
                "생성",
                css_class="helper_submit",
            )
        )

    def clean_photos(self):
        is_required = self.fields["photos"].required

        file_list: List[File] = self.cleaned_data.get("photos")
        if not file_list and is_required:
            raise forms.ValidationError("최소 1개의 사진을 등록해주세요.")
        elif file_list:
            try:
                file_list = [make_thumb(file) for file in file_list]
            except Exception as e:
                raise forms.ValidationError(
                    "썸네일 생성 중에 오류가 발생했습니다."
                ) from e
        return file_list


class NoteUpdateForm(NoteCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photos"].required = False
        self.helper.form_tag = False
        self.helper.inputs = []


class PhotoInlineForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image"]


class CustomBaseInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        if index == 0:
            form.fields["DELETE"].widget = forms.HiddenInput()


PhotoUpdateFormSet = inlineformset_factory(
    parent_model=Note,
    model=Photo,
    form=PhotoInlineForm,
    formset=CustomBaseInlineFormSet,
    extra=0,
    can_delete=True,
)
PhotoUpdateFormSet.helper = FormHelper()
PhotoUpdateFormSet.helper.form_tag = False

