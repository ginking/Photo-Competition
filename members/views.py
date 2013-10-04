from django.http import HttpResponse
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from mpc.settings import MAX_MEMBERS_ALLOWED, MIN_MEMBERS_REQUIRED, MAX_TEAMS_ALLOWED

from members.forms import Registration, ChoiceLeader

from models import Member
from teams.models import Team
from django.core.context_processors import request

def login(request):
    if request.user.is_authenticated():
        return redirect('user-profile')
    else:
        return views.login(request, template_name='login.html')

def logout(request):
    views.logout(request)
    return redirect('login')

@login_required
def user_prfile(request):
    user = Member.objects.get(username=request.user.username)
    team = Team.objects.get(id=user.team_id)
    return render_to_response('user_page.html', {'team': team, 
                                                 'user_name' : user })
#     return render(request, 'user_page.html', locals())

def game_registration(request):
    if request.method == 'POST': #is_authenticated():
        form = Registration(request.POST)
        if form.is_valid():
            form.cleaned_data['given_name']
            m = get_object_or_404(Member, name=form.cleaned_data['given_name'])
            t = Team.objects.get(id=m.team_id)
            m1 = Member.objects.filter(team_id=m.team_id)
            participant_members = len(m1.filter(is_participant=True))
            print "!!!!!!!!!!", participant_members
            print "!!!m!!", m.team_id, m.is_participant, t.is_active
            active_teams = len(Team.objects.filter(is_active=True))
            print "!!!!!!^^^!!!!", active_teams <= MAX_TEAMS_ALLOWED, participant_members <= MAX_MEMBERS_ALLOWED, m.is_participant == False 
            if active_teams <= MAX_TEAMS_ALLOWED and \
                                participant_members <= MAX_MEMBERS_ALLOWED and \
                                m.is_participant == False:
                m.update_member()
                if not t.is_active and participant_members >= MIN_MEMBERS_REQUIRED-1:
                    t.update_teams()
                print "!!!!!!!!!saved!!!!!!!!"

#             print "!!!!!!", Team.objects.
#         return HttpResponse('<h1>Page was found</h1>') #redirect('upload-teams')
    else:
        form = Registration()
#         return views.login(request, template_name='game_registration.html')
    return render_to_response('game_registration.html', {'form': form }, 
                              context_instance=RequestContext(request))

@login_required
def choice_leader(request):

    if request.method == 'POST':
        form = ChoiceLeader(request.POST, user=request.user)
        if form.is_valid():
            print "!!!!!!!!!choice!!!!!!!!!", form.cleaned_data['choice'].id
            instance = form.cleaned_data['choice']
            m = Member.objects.get(id=request.user.id)
            if not m.is_leader_voted:
                instance.score_update()
                instance.save()
                m.is_leader_voted = True
                m.save()
            return redirect('user-profile')
    form = ChoiceLeader(user=request.user)
#     member = Member.objects.get(username=request.user)
    return render_to_response('choice_leader.html', {'form': form }, 
                              context_instance=RequestContext(request))
#     return render(request, 'choice_leader.html', {'form': form})

@staff_member_required
def res_choice_leader(request):
    m = Member.objects.filter(is_participant=True).values('team_id')
    print "!!!!!!!!!m!!!!!!!!!!!", m
    team_members = Member.objects.filter(team=m.team).filter(is_participant=True)
    print "!!!!!!!!!!!!!!team_members!!!!!!!!!", team_members
    return render_to_response('res_choice_leader.html', 
                              {'team_members': team_members})



