from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView

from truthapp.decorators import reciting_ownership_required
from truthapp.forms import RecitingBoardForm
from truthapp.models import RecitingBoard


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class RecitingCreateView(CreateView):
    model = RecitingBoard
    form_class = RecitingBoardForm
    template_name = 'truthapp/create.html'
    success_url = reverse_lazy('truthapp:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        temp_reciting = form.save(commit=False)
        temp_reciting.author = self.request.user
        temp_reciting.save()
        return super().form_valid(form)


class RecitingListView(ListView):
    model = RecitingBoard
    context_object_name = 'reciting_list'
    template_name = 'truthapp/list.html'
    paginate_by = 25

    def get_queryset(self):
        return RecitingBoard.objects.all().order_by('-created_at')


@login_required
def RecitingDeleteView(request, pk):

    pilboard = get_object_or_404(RecitingBoard, pk=pk)
    pilboard.delete()

    return redirect('truthapp:list')


def index(request):
    return render(request, 'truthapp/content.html')


def bible(request):
    if request.method == "GET":
        bible_chapter = request.GET.get('bible_select')
        if bible_chapter is not None:
            if bible_chapter == "창세기":
                bible_address = "truthapp/bible/001Genesis.htm"
            elif bible_chapter == "출애굽기":
                bible_address = "truthapp/bible/002Exodus.htm"
            elif bible_chapter == "레위기":
                bible_address = "truthapp/bible/003Leviticus.htm"
            elif bible_chapter == "민수기":
                bible_address = "truthapp/bible/004Numbers.htm"
            elif bible_chapter == "신명기":
                bible_address = "truthapp/bible/005Deuteronomy.htm"
            elif bible_chapter == "여호수아":
                bible_address = "truthapp/bible/006Joshua.htm"
            elif bible_chapter == "사사기":
                bible_address = "truthapp/bible/007Judges.htm"
            elif bible_chapter == "룻기":
                bible_address = "truthapp/bible/008Ruth.htm"
            elif bible_chapter == "사무엘상":
                bible_address = "truthapp/bible/009Samuel1.htm"
            elif bible_chapter == "사무엘하":
                bible_address = "truthapp/bible/010Samuel2.htm"
            elif bible_chapter == "열왕기상":
                bible_address = "truthapp/bible/011Kings1.htm"
            elif bible_chapter == "열왕기하":
                bible_address = "truthapp/bible/012Kings2.htm"
            elif bible_chapter == "역대상":
                bible_address = "truthapp/bible/013Chronicles1.htm"
            elif bible_chapter == "역대하":
                bible_address = "truthapp/bible/014Chronicles2.htm"
            elif bible_chapter == "에스라":
                bible_address = "truthapp/bible/015Ezra.htm"
            elif bible_chapter == "느혜미아":
                bible_address = "truthapp/bible/016Nehemiah.htm"
            elif bible_chapter == "에스더":
                bible_address = "truthapp/bible/017Esther.htm"
            elif bible_chapter == "욥기":
                bible_address = "truthapp/bible/018Job.htm"
            elif bible_chapter == "시편":
                bible_address = "truthapp/bible/019Psalms.htm"
            elif bible_chapter == "잠언":
                bible_address = "truthapp/bible/020Proverbs.htm"
            elif bible_chapter == "전도서":
                bible_address = "truthapp/bible/021Ecclesiastes.htm"
            elif bible_chapter == "아가":
                bible_address = "truthapp/bible/022Songs.htm"
            elif bible_chapter == "이사야":
                bible_address = "truthapp/bible/023Isaiah.htm"
            elif bible_chapter == "예레미아":
                bible_address = "truthapp/bible/024Jeremiah.htm"
            elif bible_chapter == "예레애가":
                bible_address = "truthapp/bible/025Lamentations.htm"
            elif bible_chapter == "에스겔":
                bible_address = "truthapp/bible/026Ezekiel.htm"
            elif bible_chapter == "다니엘":
                bible_address = "truthapp/bible/027Daniel.htm"
            elif bible_chapter == "호세아":
                bible_address = "truthapp/bible/028Hosea.htm"
            elif bible_chapter == "요엘":
                bible_address = "truthapp/bible/029Joel.htm"
            elif bible_chapter == "아모스":
                bible_address = "truthapp/bible/030Amos.htm"
            elif bible_chapter == "오바댜":
                bible_address = "truthapp/bible/031Obadiah.htm"
            elif bible_chapter == "요나":
                bible_address = "truthapp/bible/032Jonah.htm"
            elif bible_chapter == "미가":
                bible_address = "truthapp/bible/033Micah.htm"
            elif bible_chapter == "나훔":
                bible_address = "truthapp/bible/034Nahum.htm"
            elif bible_chapter == "하박국":
                bible_address = "truthapp/bible/035Habakkuk.htm"
            elif bible_chapter == "스바냐":
                bible_address = "truthapp/bible/036Zephaniah.htm"
            elif bible_chapter == "학개":
                bible_address = "truthapp/bible/037Haggai.htm"
            elif bible_chapter == "스가랴":
                bible_address = "truthapp/bible/038Zechariah.htm"
            elif bible_chapter == "말라기":
                bible_address = "truthapp/bible/039Malachi.htm"
            elif bible_chapter == "마태복음":
                bible_address = "truthapp/bible/101Matthew.htm"
            elif bible_chapter == "마가복음":
                bible_address = "truthapp/bible/102Mark.htm"
            elif bible_chapter == "누가복음":
                bible_address = "truthapp/bible/103Luke.htm"
            elif bible_chapter == "요한복음":
                bible_address = "truthapp/bible/104John.htm"
            elif bible_chapter == "사도행전":
                bible_address = "truthapp/bible/105Acts.htm"
            elif bible_chapter == "로마서":
                bible_address = "truthapp/bible/106Romans.htm"
            elif bible_chapter == "고린도전서":
                bible_address = "truthapp/bible/107Corinthians1.htm"
            elif bible_chapter == "고린도후서":
                bible_address = "truthapp/bible/108Corinthians2.htm"
            elif bible_chapter == "갈라디아서":
                bible_address = "truthapp/bible/109Galatians.htm"
            elif bible_chapter == "에베소서":
                bible_address = "truthapp/bible/110Ephesians.htm"
            elif bible_chapter == "빌립보서":
                bible_address = "truthapp/bible/111Philippians.htm"
            elif bible_chapter == "골로새서":
                bible_address = "truthapp/bible/112Colossians.htm"
            elif bible_chapter == "데살전서":
                bible_address = "truthapp/bible/113Thessalonians1.htm"
            elif bible_chapter == "데살후서":
                bible_address = "truthapp/bible/114Thessalonians2.htm"
            elif bible_chapter == "디모전서":
                bible_address = "truthapp/bible/115Timothy1.htm"
            elif bible_chapter == "디모후서":
                bible_address = "truthapp/bible/116Timothy2.htm"
            elif bible_chapter == "디도서":
                bible_address = "truthapp/bible/117Titus.htm"
            elif bible_chapter == "빌레몬서":
                bible_address = "truthapp/bible/118Philemon.htm"
            elif bible_chapter == "히브리서":
                bible_address = "truthapp/bible/119Hebrews.htm"
            elif bible_chapter == "야고보서":
                bible_address = "truthapp/bible/120James.htm"
            elif bible_chapter == "베드로전서":
                bible_address = "truthapp/bible/121Peter1.htm"
            elif bible_chapter == "베드로후서":
                bible_address = "truthapp/bible/122Peter2.htm"
            elif bible_chapter == "요한일서":
                bible_address = "truthapp/bible/123John1.htm"
            elif bible_chapter == "요한이서":
                bible_address = "truthapp/bible/124John2.htm"
            elif bible_chapter == "요한삼서":
                bible_address = "truthapp/bible/125John3.htm"
            elif bible_chapter == "유다서":
                bible_address = "truthapp/bible/126Jude.htm"
            elif bible_chapter == "요한계시록":
                bible_address = "truthapp/bible/127Revelation.htm"
            return render(request, bible_address)
        else:
            return render(request, 'truthapp/content.html')
    else:

        return render(request, 'truthapp/content.html')
