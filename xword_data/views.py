from django.shortcuts import render, redirect
from django.template import Template, Context
from django.http import HttpResponse

# Create your views here.
def xword_drill(request):
    if request.method == "GET":
        # i am SUPER not positive on this HTML work
        # i love the backend, not the front end, and some G4G helped out here
        responding_html = """
    <form>
        <label for="answer">Enter your guess:</label>
        <input type="text", name="answer"/>
        <a href="{% url 'xword-answer' id=clue_id %}">Submit</a>
        <!-- ^ probably horribly wrong but idc, not an HTML dev... yet -->
    </form>
    """
        template = Template(responding_html)
        context = Context({"clue_id": 1}) # would make this a random call, but
        # i don't know how many clues we have! don't want to make unnecessary
        # calls just to find out

        return HttpResponse(template.render(context))

    # S: this implementation is not great, but Django has forced my hand
    from .models import Clue

    data = request.POST # get the info from whoever's POSTing
    answer = data["answer"].upper() # complying with the roolz
    clue_object = Clue.objects.get(pk=data["clue_id"])
    if clue_object.entry.entry_text != answer:
        return HttpResponse(f"<p>{data["answer"].upper()} is not correct!</p>")
        # try again, you got this!

    return redirect("xword-answer", id=data["clue_id"])
    # may or may not be botched redirect call

def xword_answer(request, id):
    # S: again, Django has forced my hand
    from .models import Clue

    # i would LOVE to know how to determine what the tag is for testing
    # and how to handle it, however, researching has dug up some pretty empty
    # caskets of others having the same issues that i can't quite understand

    # i work best with code existing, and a LOT of it, dangit

    objects = Clue.objects.values()


    # quick 404 check
    dict_to_work_with = {}
    for diction in objects:
        if diction["id"] == id:
            dict_to_work_with = diction
            break

    if len(dict_to_work_with.keys())<1:
        response = HttpResponse()
        response.status_code = 404
        return response

    # ok we good

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

    # ^ close enough zip, it worked out in the end

    lst = list(range(max(ids))) # stdio magic, not even i remember what this was for fully
    working_lst = [0 for _unused in range(len(lst))]
    #                    ^ complying with naming scheme

    for item in ids:
        working_lst[item-1] += 1

    # could i instead make this into something involving list's count function?
    # maybe. however, i do not care enough to lmao

    html_response = f"""
    <p>{Clue.objects.get(pk=id).entry.entry_text} is the correct answer! You have now answered 1 (of 3) clues correctly.</p>
<table>
    <tr>
        <th>Count</th>
        <th>Entry</th>
    </tr>
        """
    # weaving together an HTML on the fly
    # HTML3 wishes it was me
    for name, count in sorted_zip:
        html_response += f"""
    <tr>
        <td>{count}</td>
        <td>{name}</td>
    </tr>
"""
    html_response += "</table>"

    # final check to determine whether or not we should slap it in there
    # this is a testing call, so i think it's okay to have it down at the bottom

    if id in ids:
        quick_and_dirty_check = Clue.objects.get(pk=id)
        entry_ids = [item["entry_id"] for item in objects]
        if entry_ids.count(quick_and_dirty_check.entry_id) == 1:
            html_response += "\n<p> only appearance of this clue </p>"

    template = Template(html_response)
    context = Context({"hi": ":3"}) # django forces my hand for the third time
    return HttpResponse(template.render(context))
