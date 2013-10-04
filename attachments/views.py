from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Attachment
from .forms import UploadPhotoForm
from members.models import Member
from teams.models import Team
from categories.models import Category


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            request_member = Member.objects.get(username=request.user)
            request_member_team = Team.objects.get(id=request_member.team_id)
#             c = form.cleaned_data['photo_category']
            chose_category = Category.objects.get(id=form.cleaned_data['photo_category'])
            print "******************", chose_category
#             c = get_object_or_404(Category, category_name=form.cleaned_data['photo_category'])
            print "############################", request_member, request_member_team, chose_category
            instance = Attachment(photo_file=request.FILES['photo_file'], 
                                team_owner=request_member_team,
                                member_owner=request_member,
                                category=chose_category)
            instance.save()
            return redirect('user-profile')
    else:
        form = UploadPhotoForm()
    member = Member.objects.get(username=request.user)
    return render(request, 'upload_photo.html', {'form': form,
                                                 'member' : member})


def all_photos(request):
    attachments = Attachment.objects.all()
    return render(request, 'all_photos.html', {'attachments' : attachments})

