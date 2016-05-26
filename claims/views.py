from django.shortcuts import render, redirect
from .forms import ClaimForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def addClaim(request):
	title = "Make a Claim"
	form = ClaimForm(request.POST or None)
	if form.is_valid():
		#get stuff from form
		form_title = form.cleaned_data.get("title")
		form_claim = form.cleaned_data.get("claimcontent")
		form_source = form.cleaned_data.get("source")

		#save to database
		claim = form.save(commit=False)
		claim.user = request.user
		claim.user_id = request.user.id
		claim.save()
		form.save_m2m() # http://django-taggit.readthedocs.org/en/latest/forms.html

		#increment authority
		user_id = request.user.id
		user = User.objects.get(pk = user_id).standarduser
		user.authority += 1
		user.save()

		#email stuff
		subject = 'New Contribution!'
		from_email = settings.EMAIL_HOST_USER
		to_email = ["clarkbristol@gmail.com"]
		contact_message = """
			%s: %s
			""" % (form_title,form_claim)
		send_mail(subject,
			contact_message,
			from_email,
			to_email,
			fail_silently=False)
		return redirect("http://localhost:8000/browseClaims/")
	
	context = {
		"form": form,
		"title": title,
	}

	return render(request, "forms.html", context)


from django.views.generic.list import ListView
from claims.models import Claim

class ClaimListView(ListView):
    model = Claim

def get_context_data(self, **kwargs):
    context = super(ClaimListView, self).get_context_data(**kwargs)
    return context

















