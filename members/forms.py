from django import forms

from members.models import Member


class Registration(forms.Form):
    given_name = forms.CharField()


class ChoiceLeader(forms.Form):
    choice = forms.ModelChoiceField(queryset=Member.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChoiceLeader, self).__init__(*args, **kwargs)
        if user:
            m = Member.objects.get(id=user.id)
            team_members = Member.objects.filter(team=m.team).filter(is_participant=True)
            print "team_membersteam_membersteam_members", team_members
            self.fields['choice'] = forms.ModelChoiceField(queryset=team_members,
                                                           widget=forms.RadioSelect,
                                                           empty_label=None)
