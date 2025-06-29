from django.contrib import admin

from .models import Choice, Question

admin.site.site_header = "Poll App"
class ChoiceInline(admin.TabularInline): 
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
      list_display = ["question_text", "pub_date", "was_published_recently"]
      inlines = [ChoiceInline]
      list_filter = ["pub_date"]
      search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)