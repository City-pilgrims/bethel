from django.contrib import admin
from .models import TimelineEvent, PilgrimBoard, Question, Answer

admin.site.register(TimelineEvent)

admin.site.register(PilgrimBoard)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_secret', 'is_answered', 'views', 'created_at']
    list_filter = ['category', 'is_secret', 'is_answered', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['views', 'created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'content', 'category', 'author')
        }),
        ('비밀글 설정', {
            'fields': ('is_secret', 'password'),
            'classes': ('collapse',)
        }),
        ('상태 정보', {
            'fields': ('is_answered', 'views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:  # 수정 시
            readonly_fields.append('author')
        return readonly_fields


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'is_official', 'created_at']
    list_filter = ['is_official', 'created_at']
    search_fields = ['content', 'question__title', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('기본 정보', {
            'fields': ('question', 'content', 'author')
        }),
        ('설정', {
            'fields': ('is_official',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:  # 수정 시
            readonly_fields.extend(['question', 'author'])
        return readonly_fields