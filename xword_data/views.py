from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse

# Create your views here.
def xword_drill(request):
    blurgh = "<!-- something, alright -->"
    template = Template(blurgh)
    context = Context({"clue_id":1})

    return HttpResponse(template.render(context))

def xword_answer(request, id):
    return HttpResponse()
