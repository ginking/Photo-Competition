from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.context_processors import request
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

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

def game_registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            form.cleaned_data['given_name']
            reg_member = get_object_or_404(Member, name=form.cleaned_data['given_name'])
            reg_member_team = Team.objects.get(id=reg_member.team_id)
            get_team_members = Member.objects.filter(team_id=reg_member.team_id)
            participant_members = len(get_team_members.filter(is_participant=True))
            active_teams = len(Team.objects.filter(is_active=True))

            if active_teams < MAX_TEAMS_ALLOWED and \
                                participant_members < MAX_MEMBERS_ALLOWED and \
                                reg_member.is_participant == False:
                reg_member.update_member()
                participant_members += 1
                if not reg_member_team.is_active and participant_members >= MIN_MEMBERS_REQUIRED-1:
                    reg_member_team.update_teams()

    else:
        form = Registration()

    return render_to_response('game_registration.html', {'form': form }, 
                              context_instance=RequestContext(request))

@login_required
def choice_leader(request):
    if request.method == 'POST':
        form = ChoiceLeader(request.POST, user=request.user)
        if form.is_valid():
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

    return render_to_response('choice_leader.html', {'form': form }, 
                              context_instance=RequestContext(request))

@staff_member_required
def res_choice_leader(request):
    set_of_team_id = set()
    list_of_team_id = Member.objects.filter(is_participant=True).values('team_id')
    for i in list_of_team_id:
        set_of_team_id.add(i['team_id'])
    max_scored_members = {}
    for tid in set_of_team_id:
        max_scored_members.update({tid : Member.objects.filter(team_id=tid).filter(is_participant=True).order_by('-score')[0]})

    active_teams = Team.objects.filter(is_active=True)
    for i in active_teams:
        inst = max_scored_members[i.id]
        Member.objects.filter(team_id=i.id).update(is_leader=False)
        inst.is_leader=True
        inst.save()
    leaders = Member.objects.filter(is_leader=True)
    return render_to_response('res_choice_leader.html', 
                              {'leaders': leaders})

