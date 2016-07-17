from django.shortcuts import render, redirect
from .forms import ClaimForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
# EXPERIMENT W/ NEO4J
from py2neo import authenticate, Graph, Node

def addClaim(request):
	title = "Make a Claim"
	form = ClaimForm(request.POST or None)
	if form.is_valid():
		#get stuff from form
		form_name = form.cleaned_data.get("name")
		form_content = form.cleaned_data.get("content")
		form_source = form.cleaned_data.get("source")

		#save to database
		claim = form.save(commit=False)
		claim.user = request.user
		claim.user_id = request.user.id
		claim.save()
		form.save_m2m() # http://django-taggit.readthedocs.org/en/latest/forms.html

		#increment authority
		user_id = request.user.id
		print(user_id)
		print(User.objects.get(pk = user_id))
		user = User.objects.get(pk = user_id).standarduser
		user.authority += 1
		user.save()

		#email stuff
		subject = 'New Contribution!'
		from_email = settings.EMAIL_HOST_USER
		to_email = ["clarkbristol@gmail.com"]
		contact_message = """
			%s: %s
			""" % (form_name,form_content)
		send_mail(subject,
			contact_message,
			from_email,
			to_email,
			fail_silently=False)

		# make a neo4j node
		authenticate("localhost:7474", "neo4j", "cbristol")
		graph = Graph()
		claim = Node("Claim", name=form_name, content=form_content)
		graph.create(claim)
		
		return redirect("http://localhost:8000/claims/")
	
	context = {
		"form": form,
		"title": title,
	}

	return render(request, "forms.html", context)



def viewClaim(request,claim_id):
	try:
		c = Claim.objects.get(pk=claim_id)
	except Claim.DoesNotExist:
		raise Http404("Claim does not exist")
	return render(request, "claims/viewClaim.html", {'claim': c})	



from django.views.generic.list import ListView
from claims.models import Claim

class ClaimListView(ListView):
    model = Claim

def get_context_data(self, **kwargs):
    context = super(ClaimListView, self).get_context_data(**kwargs)
    return context

















