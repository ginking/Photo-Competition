from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

from teams.models import Team
from members.models import Member

from teams.forms import UploadFileForm


def handle_uploaded_file(file):

    for chunk in file.chunks():
        team_rows = chunk.split('\n')
        teams = team_rows[0].split(',')
        for t in teams:
            instance = Team.objects.create(team_name=t)
            instance.save()

        i = 0
        for members in team_rows[1:]:
            list_of_members = members.split(',')
            print "!!!!!!!!!!!!!!1", list_of_members
            for member in list_of_members:
                i += 1
                team = Team.objects.get(id=i)
                first_last_name = member.split(' ')
                usrname = ''.join(first_last_name)
                if usrname != "":
                    inst = Member.objects.create_user(username=usrname, password=usrname,
                                                      name=member, team_id=team.id)
#                 inst.save()
            i = 0


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
