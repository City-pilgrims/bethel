from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import CreateView, DeleteView

from commentapp.decorators import comment_ownership_required
from commentapp.forms import CommentCreationForm
from commentapp.models import Comment
from wayapp.models import Note


from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView

from commentapp.decorators import comment_ownership_required
from commentapp.forms import CommentCreationForm
from commentapp.models import Comment
from wayapp.models import Note


@csrf_exempt
def CommentCreateView(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content","").strip()
            note = get_object_or_404(Note, pk=data["note_pk"])

            if not content:
                return JsonResponse({"success": False, "error": "댓글을 입력하세요."}, status=400)

            # 트랜잭션 적용하여 강제 커밋
            with transaction.atomic():
                comment = Comment.objects.create(
                    note=note,
                    author=request.user,  # user 인증 필요
                    content=data["content"]
                )

            return JsonResponse({
                "success": True,
                "comment_id": comment.id,
                "note_pk": comment.note.pk,
                "author": comment.author.username,
                "content": comment.content,
                "created_at": localtime(comment.created_at).strftime("%Y-%m-%d %H:%M")
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False}, status=400)


@login_required
def CommentDeleteView(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)

        # 현재 로그인한 사용자가 댓글 작성자인지 확인
        if comment.author == request.user:
            note_pk = comment.note.pk
            comment.delete()
            return JsonResponse({"success": True, "comment_id": pk, "note_pk": note_pk})
        return JsonResponse({"success": False, "error": "권한이 없습니다."}, status=403)
    return JsonResponse({"success": False, "error": "잘못된 요청입니다"}, status=400)

