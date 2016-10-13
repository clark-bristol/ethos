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

#############################################################################
############################  Webpage Views #################################
#############################################################################


############################  Claim Form #################################
# @login_required
# @csrf_exempt
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
        print this_users_affirmations

        # get list of affirmations to pass to template renderer
        user = User.objects.get(pk=request.user.id).standarduser
        user.authority += 1
        user.save()

        # create affirmation
        # new_affirmation = Affirmation(claim=new_claim, user=new_claim.creator_user)
        # new_affirmation.save()

        # connect to graph, start and commit new transaction
        authenticate("localhost:7474", "neo4j", "cbristol")
        claim = Node("Claim", claim_id=new_claim.id, name=new_claim.name, content=new_claim.content)
        user = Node("User", user_id=request.user.id, name=request.user.username)
        subgraph = claim | user
        graph = Graph()
        tx = graph.begin()
        tx.merge(subgraph, primary_label='name')
        tx.commit()

        return redirect("http://localhost:8000/claims/" + str(new_claim.pk))

    title = "Make a Claim"
    context = {
        "form": form,
        "title": title,
    }

    return render(request, "forms.html", context)


############################  Argument Form #################################
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
            ArgumentPremise.objects.create(claim_id=int(claim_id), argument = new_argument)

        # Neo4J Stuff
        authenticate("localhost:7474", "neo4j", "cbristol")
        argument_graph = Node("Argument", argument_id=new_argument.id, name=new_argument.name)
        subgraph = argument_graph

        for argumentPremise in ArgumentPremise.objects.filter(argument_id=new_argument.id):
            premiseClaim = argumentPremise.claim
            premiseClaim_graph = Node("Claim", claim_id=premiseClaim.id, name=premiseClaim.name, content=premiseClaim.content)
            premise_of_graph = Relationship(premiseClaim_graph, "Premise_Of", argument_graph)
            subgraph = subgraph | premiseClaim_graph | premise_of_graph
            # ArgumentPremise.objects.create(claim_id=int(claim_id), argument = new_argument)

        supportedClaim = new_argument.supported_claim
        print supportedClaim
        supportedClaim_graph = Node("Claim", claim_id=supportedClaim.id, name=supportedClaim.name, content=supportedClaim.content)
        supports_graph = Relationship(argument_graph, "Supports", supportedClaim_graph)
        subgraph = subgraph | supportedClaim_graph | supports_graph

        graph = Graph()
        tx = graph.begin()
        tx.merge(subgraph, primary_label='name')
        tx.commit()

        # for premise_claim in new_argument.premise_claims
            # premise = Relationship(argumentPremise, "Premise", argument)

        # # connect to graph, start and commit new transaction
        # authenticate("localhost:7474", "neo4j", "cbristol")
        # claim = Node("Claim", claim_id=new_claim.id, name=new_claim.name, content=new_claim.content)
        # user = Node("User", user_id=request.user.id)
        # affirms = Relationship(user, "Affirms", claim)
        # subgraph = claim | user | affirms
        # graph = Graph()
        # tx = graph.begin()
        # tx.merge(subgraph, primary_label='name')
        # # tx.merge(subgraph3, primary_label='user_id')
        # tx.commit()

        return redirect("http://localhost:8000/arguments/")

    title = "Make an Argument!"
    context = {
        "form": form,
        "title": title,
    }

    return render(request, "forms.html", context)


############################  View Claim #################################
def viewClaim(request, claim):
    context = {}

    try:
        this_claim = Claim.objects.get(pk=claim)
    except Claim.DoesNotExist:
        raise Http404("Claim does not exist")

    try:
        context["affirmation"] = Affirmation.objects.get(claim_id=claim,user_id=request.user)
    except Affirmation.DoesNotExist:
        context["affirmation"] = None

    context["claim"] = this_claim
    context["num_affirmations"] = Affirmation.objects.filter(claim_id=claim).count()

    # print context

    return render(request, "claims/viewClaim.html", context)


############################  View Argument #################################
def viewArgument(request, argument):
    context = {}

    try:
        this_argument = Argument.objects.get(pk=argument)
    except Argument.DoesNotExist:
        raise Http404("Argument does not exist")

    context["argument"] = this_argument

    print context

    return render(request, "claims/viewArgument.html", context)


############################  List all Claims #################################
class ClaimListView(ListView):
    model = Claim


############################  List all Arguments #################################
class ArgumentListView(ListView):
    model = Argument


#############################################################################
################ API Views: Users, Claims, Affirmations #####################
#############################################################################


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
        # print serializer
        if serializer.is_valid():
            serializer.save()

            # connect to graph, start and commit new transaction
            print serializer.validated_data
            affirmed_claim = serializer.validated_data["claim"]
            affirming_user = serializer.validated_data["user"]

            authenticate("localhost:7474", "neo4j", "cbristol")
            affirmed_claim_graph = Node("Claim", claim_id=affirmed_claim.id, name=affirmed_claim.name, content=affirmed_claim.content)
            affirming_user_graph = Node("User", user_id=affirming_user.id, name=affirming_user.username)
            affirms = Relationship(affirming_user_graph, "Affirms", affirmed_claim_graph)
            subgraph = affirmed_claim_graph | affirming_user_graph | affirms
            graph = Graph()
            tx = graph.begin()
            tx.merge(subgraph, primary_label='name')
            # tx.merge(subgraph3, primary_label='user_id')
            tx.commit()

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
        affirmation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

