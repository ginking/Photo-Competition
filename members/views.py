from django.http import HttpResponse
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.context_processors import request

from mpc.settings import MAX_MEMBERS_ALLOWED, MIN_MEMBERS_REQUIRED, MAX_TEAMS_ALLOWED

from members.forms import Registration, ChoiceLeader

from models import Member
from teams.models import Team


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
            reg_member = get_object_or_404(Member, name=form.cleaned_data['given_name'])
            reg_member_team = Team.objects.get(id=reg_member.team_id)
            get_team_members = Member.objects.filter(team_id=reg_member.team_id)
            participant_members = len(get_team_members.filter(is_participant=True))
            print "!!!!!!!!!!", participant_members
            print "!!!m!!", reg_member.team_id, reg_member.is_participant, reg_member_team.is_active
            active_teams = len(Team.objects.filter(is_active=True))
            print "!!!!!!^^^!!!!", active_teams <= MAX_TEAMS_ALLOWED, participant_members <= MAX_MEMBERS_ALLOWED, reg_member.is_participant == False 
            if active_teams < MAX_TEAMS_ALLOWED and \
                                participant_members < MAX_MEMBERS_ALLOWED and \
                                reg_member.is_participant == False:
                reg_member.update_member()
                participant_members += 1
                if not reg_member_team.is_active and participant_members >= MIN_MEMBERS_REQUIRED-1:
                    reg_member_team.update_teams()
#                     active_teams += 1
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
            elected_member = form.cleaned_data['choice']
            request_member = Member.objects.get(id=request.user.id)
            if not request_member.is_leader_voted and request_member.is_participant:
                elected_member.score_update()
                elected_member.save()
                request_member.is_leader_voted = True
                if elected_member.id == request_member.id:
                    request_member.score += 1
                request_member.save()
            return redirect('user-profile')
    form = ChoiceLeader(user=request.user)
#     member = Member.objects.get(username=request.user)
    return render_to_response('choice_leader.html', {'form': form }, 
                              context_instance=RequestContext(request))
#     return render(request, 'choice_leader.html', {'form': form})

@staff_member_required
def res_choice_leader(request):

    set_of_team_id = set()
    list_of_team_id = Member.objects.filter(is_participant=True).values('team_id')
    for i in list_of_team_id:
        set_of_team_id.add(i['team_id'])
    print "!!!!!!!!!set_of_team_id!!!!!!!!!!!", set_of_team_id
    max_scored_members = {}
    for tid in set_of_team_id:
        max_scored_members.update({tid : Member.objects.filter(team_id=tid).filter(is_participant=True).order_by('-score')[0]})
    print "!!!!!!!!!!!l!!!!!!!!!!!!!!!", max_scored_members

    active_teams = Team.objects.filter(is_active=True)
    for i in active_teams:
        inst = max_scored_members[i.id]
        Member.objects.filter(team_id=i.id).update(is_leader=False)
        inst.is_leader=True
        inst.save()
    leaders = Member.objects.filter(is_leader=True)
#     Member.objects.filterfilter(team_id=m.team).filter(is_participant=True)
#     team_members = Member.objects.filter(team=m.team).filter(is_participant=True)
#     print "!!!!!!!!!!!!!!team_members!!!!!!!!!", team_members
    return render_to_response('res_choice_leader.html', 
                              {'leaders': leaders})



