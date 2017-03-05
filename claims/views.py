from django.shortcuts import render, redirect
from .forms import ClaimForm, ArgumentForm
from django.contrib.auth.models import User
from django.http import Http404
from claims.models import Claim, Argument, ArgumentPremise
# Neo4J
from py2neo import authenticate, Graph, Node, Relationship
# List view
from django.views.generic.list import ListView
# import decorators for experimenting
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# API!
from claims.models import Claim, Affirmation
from claims.serializers import UserSerializer, ClaimSerializer, AffirmationSerializer
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
# functions!
from functions import addClaimToGraph
from functions import addUserToGraph
from functions import addArgumentToGraph
from functions import addAffirmationToGraph
from functions import removeAffirmationFromGraph
from functions import sync_graph


# Webpage Views


# Claim Form
@require_http_methods(["GET", "POST"])
def addClaim(request):
    form = ClaimForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # save to pg database
        new_claim = form.save(commit=False)
        new_claim.save()

        # increment authority
        this_users_affirmations = []
        for e in Affirmation.objects.filter(user_id=request.user.id).order_by('claim_id'):
            this_users_affirmations.append(e.claim_id)
        print(this_users_affirmations)

        # get list of affirmations to pass to template renderer
        user = User.objects.get(pk=request.user.id).standarduser
        user.authority += 1
        user.save()

        addClaimToGraph(new_claim)
        addUserToGraph(request.user)

        return redirect("http://localhost:8000/claims/" + str(new_claim.pk))

    title = "Make a Claim"
    context = {
        "form": form,
        "title": title,
    }

    return render(request, "forms.html", context)


# Argument Form
# @login_required
# @csrf_exempt
@require_http_methods(["GET", "POST"])
def addArgument(request):
    form = ArgumentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # save to pg database
        new_argument = form.save(commit=False)
        new_argument.save()

        for claim_id in request.POST.getlist('premise_claims'):
            ArgumentPremise.objects.create(claim_id=int(claim_id), argument=new_argument)

        addArgumentToGraph(new_argument, request.user)

        return redirect("http://localhost:8000/arguments/")

    title = "Make an Argument!"
    context = {
        "form": form,
        "title": title,
    }

    return render(request, "forms.html", context)


# View Claim
def viewClaim(request, claim):

    if request.user.is_authenticated():
        sync_graph(user=request.user)

    context = {}

    try:
        this_claim = Claim.objects.get(pk=claim)
    except Claim.DoesNotExist:
        raise Http404("Claim does not exist")

    try:
        context["affirmation"] = Affirmation.objects.get(claim_id=claim, user_id=request.user)
    except Affirmation.DoesNotExist:
        context["affirmation"] = None

    context["claim"] = this_claim
    context["num_affirmations"] = Affirmation.objects.filter(claim_id=claim).count()
    context["supporting_arguments"] = Argument.objects.filter(supported_claim_id=claim)
    # context["suggested_claims"] =

    return render(request, "claims/viewClaim.html", context)


# View Argument
def viewArgument(request, argument):
    context = {}

    try:
        this_argument = Argument.objects.get(pk=argument)
    except Argument.DoesNotExist:
        raise Http404("Argument does not exist")

    context["argument"] = this_argument

    return render(request, "claims/viewArgument.html", context)


# List all Claims
class ClaimListView(ListView):
    model = Claim


# List all Arguments
class ArgumentListView(ListView):
    model = Argument


#
# API Views: Users, Claims, Affirmations #####################
#


# API Views: Users

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# API Views: Users

@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete an user instance.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API Views: Claims

@api_view(['GET', 'POST'])
def claim_list(request):
    """
    List all claims, or create a new claim.
    """
    if request.method == 'GET':
        claims = Claim.objects.all()
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClaimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def claim_detail(request, pk):
    """
    Retrieve, update or delete an claim instance.
    """
    try:
        claim = Claim.objects.get(pk=pk)
    except Claim.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClaimSerializer(claim)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClaimSerializer(claim, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        claim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API Views: Affirmations

@api_view(['GET', 'POST'])
def affirmation_list(request):
    """
    List all affirmations, or create a new affirmation.
    """
    if request.method == 'GET':
        affirmations = Affirmation.objects.all()
        serializer = AffirmationSerializer(affirmations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AffirmationSerializer(data=request.data)
        if serializer.is_valid():
            affirmation = serializer.save()

            addAffirmationToGraph(affirmation)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def affirmation_detail(request, pk):
    """
    Retrieve, update or delete an affirmation instance.
    """
    try:
        affirmation = Affirmation.objects.get(pk=pk)
    except Affirmation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AffirmationSerializer(affirmation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AffirmationSerializer(affirmation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        removeAffirmationFromGraph(affirmation)
        affirmation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
