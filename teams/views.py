# from django.contrib.auth import views, authenticate
# from django.contrib.auth import login as original_login
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# 
from teams.models import Team
from members.models import Member
# from teams.forms import DocumentForm

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

from teams.forms import UploadFileForm


def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:

    for chunk in f.chunks():
        team_rows = chunk.split('\n')
        teams = team_rows[0].split(',')
        for t in teams:
            instance = Team.objects.create(team_name=t)
            instance.save()

        i = 0
        for m in team_rows[1:]:
            am = m.split(',')
            print "!!!!!!!!!!!!!!1", am
            for a in am:
                i += 1
                t = Team.objects.get(id=i)
                sp = a.split(' ')
                j = ''.join(sp)
                if j != "":
                    inst = Member.objects.create_user(username=j, password=j,
                                                      name=a, team_id=t.id)
#                 inst.save()
            i = 0
#             destination.write(chunk)


@staff_member_required
def upload_teams(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print "!!!!!!!!!!!!", request.FILES, request.FILES['groups']
            handle_uploaded_file(request.FILES['groups'])
    else:
        form = UploadFileForm()
    return render_to_response('upload_teams.html', {'form': form}, 
                              context_instance=RequestContext(request))

# def upload_teams(request):
# 
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Team(team_file = request.FILES['team_file'])
#             newdoc.save()
# 
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('teams.views.upload_teams'))
#     else:
#         form = DocumentForm() # A empty, unbound form
# 
#     # Load documents for the list page
#     documents = Team.objects.all()
# 
#     # Render list page with the documents and the form
#     return render_to_response(
#         'upload_teams.html',
#         {'documents': documents, 'form': form},
#         context_instance=RequestContext(request)
#     )