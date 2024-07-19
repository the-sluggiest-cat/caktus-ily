from django.shortcuts import render, redirect
from django.template import Template, Context
from django.http import HttpResponse
import random

# Create your views here.
def xword_drill(request):
    # S: complicated, complicated... i can do this.
    if request.method == "GET":
        responding_html = """
    <form>
        <label for="answer">Enter your guess:</label>
        <input type="text", name="answer"/>
        <a href="{% url 'xword-answer' id=clue_id %}">Submit</a>
        <!-- ^ probably horribly wrong but idc, not an HTML dev... yet -->
    </form>
    """
        template = Template(responding_html)
        context = Context({"clue_id": 1})

        return HttpResponse(template.render(context))

    # S: this implementation is not great, but Django has forced my hand
    from .models import Clue

    data = request.POST
    answer = data["answer"].upper()
    clue_object = Clue.objects.get(pk=data["clue_id"])
    if clue_object.entry.entry_text != answer:
        return HttpResponse(f"<p>{data["answer"].upper()} is not correct!</p>")

    return redirect("xword-answer", id=data["clue_id"])

def xword_answer(request, id):
    # S: again, Django has forced my hand
    from .models import Clue

    if request.method == "GET":
        objects = Clue.objects.values()
        entry_ids = [item["id"] for item in objects]
        names = [Clue.objects.get(pk=id).entry.entry_text for id in entry_ids]
        name_count = {}
        for name in names:
            if name not in name_count.keys():
                name_count[name]  = 1
            else:
                name_count[name] += 1

        # S: we don't do any sorting here but whatever python god is smiting me...
        # i don't appreciate it..........
        sorted_names = tuple(name_count)
        sorted_values = list(sorted(name_count.values(), reverse=True))
        sorted_zip = tuple(zip(sorted_names, sorted_values))

        lst = list(range(max(entry_ids)))
        working_lst = [0 for _unused in range(len(lst))]

        for item in entry_ids:
            working_lst[item-1] += 1

        dict_to_work_with = {}
        for diction in objects:
            if diction["id"] == id:
                dict_to_work_with = diction
                break

        if len(dict_to_work_with.keys())<1:
            response = HttpResponse()
            response.status_code = 404
            return response

        html_response = """
<table>
    <tr>
        <th>Count</th>
        <th>Entry</th>
    </tr>
        """
        for name, count in sorted_zip:
            html_response += f"""
    <tr>
        <td>{count}</td>
        <td>{name}</td>
    </tr>
"""
        html_response += "</table>"

        template = Template(html_response)
        context = Context({"hi": ":3" if max(entry_ids)>1 else "only appearance of this clue"})
        return HttpResponse(template.render(context))

    print(request.POST)
    return HttpResponse()
