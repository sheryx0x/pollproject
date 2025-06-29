from django.http import HttpResponse
from .models import Question , Choice
from django.template import loader
from django.shortcuts import render , get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone





class IndexView(generic.ListView):
    template_name = "pollapp/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
            return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "pollapp/detail.html"
    
    def get_queryset(self):
        
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "pollapp/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "pollapp/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("pollapp:results", args=(question.id,)))
    
    

