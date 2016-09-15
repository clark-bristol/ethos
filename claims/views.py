from django.shortcuts import render, redirect
from .forms import ClaimForm
from django.contrib.auth.models import User
from django.http import Http404
from claims.models import Claim
# Neo4J
from py2neo import authenticate, Graph, Node, Relationship
# List view
from django.views.generic.list import ListView
# import decorators for experimenting
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# API!
from claims.models import Affirmation
from claims.serializers import UserSerializer, ClaimSerializer, AffirmationSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


# API Views

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'claims': reverse('claim-list', request=request, format=format),
        'affirmations': reverse('affirmation-list', request=request, format=format)
    })


class UserList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClaimList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class ClaimDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AffirmationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Affirmation.objects.all()
    serializer_class = AffirmationSerializer


class AffirmationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Affirmation.objects.all()
    serializer_class = AffirmationSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Other Views

# @login_required
# @csrf_exempt
@require_http_methods(["GET", "POST"])
def addClaim(request):
    form = ClaimForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # save to pg database
        new_claim = form.save(commit=False)
        new_claim.user = request.user
        new_claim.save()

        # increment authority
        user = User.objects.get(pk=request.user.id).standarduser
        user.authority += 1
        user.save()

        # create affirmation
        new_affirmation = Affirmation(claim=new_claim, user=new_claim.user)
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


# @login_required
# def affirmClaim(request, claim_id):
#     affirmation = Affirmation(user=request.user, claim=Claim.objects.get(pk=claim_id))
#     # data = AffirmationSerializer.serialize('json', affirmation)
#     return JsonResponse(affirmation)


def viewClaim(request, claim):
    try:
        c = Claim.objects.get(pk=claim)
        affirmations = Affirmation.objects.filter(claim_id=claim).count()
        contrib_user_name = User.objects.get(id=c.user.id).username
    except Claim.DoesNotExist:
        raise Http404("Claim does not exist")

    return render(request, "claims/viewClaim.html", {'claim': c, 'affirmations': affirmations, 'contrib_user_name': contrib_user_name})


class ClaimListView(ListView):
    model = Claim


# def get_context_data(self, **kwargs):
#     context = super(ClaimListView, self).get_context_data(**kwargs)
#     return context
