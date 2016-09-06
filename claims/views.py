from django.shortcuts import render, redirect
from .forms import ClaimForm
from django.contrib.auth.models import User
# EXPERIMENT W/ NEO4J
from py2neo import authenticate, Graph, Node, Relationship
#
from django.views.generic.list import ListView
from claims.models import Claim, Affirmation


def addClaim(request):
    form = ClaimForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # save to pg database
        new_claim = form.save(commit=False)
        new_claim.contrib_user = request.user
        new_claim.save()

        # increment authority
        user = User.objects.get(pk=request.user.id).standarduser
        user.authority += 1
        user.save()

        # create affirmation
        new_affirmation = Affirmation(claim=new_claim, user=new_claim.contrib_user)
        new_affirmation.save()

        # connect to graph, start and commit new transaction
        authenticate("localhost:7474", "neo4j", "cbristol")
        claim = Node("Claim", claim_id=new_claim.id, name=new_claim.name, content=new_claim.content)
        user = Node("User", user_id=request.user.id)
        affirms = Relationship(user, "Affirms", claim)
        subgraph = claim | user | affirms
        graph = Graph()
        tx = graph.begin()
        tx.merge(subgraph, primary_label='name')
        # tx.merge(subgraph3, primary_label='user_id')
        tx.commit()

        return redirect("http://localhost:8000/claims/" + str(new_claim.pk))

    title = "Make a Claim"
    context = {
        "form": form,
        "title": title,
    }

    return render(request, "forms.html", context)


def viewClaim(request, claim):
    try:
        c = Claim.objects.get(pk=claim)
    except Claim.DoesNotExist:
        raise Http404("Claim does not exist")
    return render(request, "claims/viewClaim.html", {'claim': c})


class ClaimListView(ListView):
    model = Claim


# def get_context_data(self, **kwargs):
#     context = super(ClaimListView, self).get_context_data(**kwargs)
#     return context
