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
            m = Member.objects.get(username=request.user)
            t = Team.objects.get(id=m.team_id)
#             c = form.cleaned_data['photo_category']
            c = Category.objects.get(id=form.cleaned_data['photo_category'])
            print "******************", c
#             c = get_object_or_404(Category, category_name=form.cleaned_data['photo_category'])
            print "############################", m, t, c
            instance = Attachment(photo_file=request.FILES['photo_file'], 
                                team_owner=t,
                                member_owner=m,
                                category=c)
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

