from django.shortcuts import render, redirect
from django.template import Template, Context
from django.http import HttpResponse

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

    objects = Clue.objects.values()
    ids = [item["id"] for item in objects]
    names = [Clue.objects.get(pk=id).entry.entry_text for id in ids]
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

    lst = list(range(max(ids)))
    working_lst = [0 for _unused in range(len(lst))]

    for item in ids:
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

    html_response = f"""
    <p>{Clue.objects.get(pk=id).entry.entry_text} is the correct answer! You have now answered 1 (of 3) clues correctly.</p>
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

    if id in ids:
        quick_and_dirty_check = Clue.objects.get(pk=id)
        entry_ids = [item["entry_id"] for item in objects]
        if entry_ids.count(quick_and_dirty_check.entry_id) == 1:
            html_response += "\n<p> only appearance of this clue </p>"

    template = Template(html_response)
    context = Context({"hi": ":3"})
    return HttpResponse(template.render(context))
