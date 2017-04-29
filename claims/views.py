from django.shortcuts import render, redirect
from .forms import ClaimForm, ArgumentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from claims.models import Claim, Argument, ArgumentPremise, Affirmation
# List view
from django.views.generic.list import ListView
# import decorators for experimenting
from django.views.decorators.http import require_http_methods
# API!
from claims.serializers import UserSerializer
from claims.serializers import ClaimSerializer
from claims.serializers import AffirmationSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
# functions!
from . import functions as fcns
# from functions import addClaimToGraph
# from functions import addUserToGraph
# from functions import addArgumentToGraph
# from functions import addAffirmationToGraph
# from functions import removeAffirmationFromGraph
# from functions import sync_graph

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

        fcns.addClaimToGraph(new_claim)
        fcns.addUserToGraph(request.user)

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

        fcns.addArgumentToGraph(new_argument)

        return redirect("http://localhost:8000/arguments/")

    title = "Make an Argument!"
    context = {
        "form": form,
        "title": title,
    }

    return render(request, "forms.html", context)


# View Claim
def ClaimView(request, claim):

    if request.user.is_authenticated():
        fcns.sync_graph(user=request.user)

    context = {}

    # building context varianle for vue.js
    context["vue_claims"] = []
    # for i, claim in enumerate(Claim.objects.get(pk=claim)):
    context["vue_claims"].append({"claim": None,
                                  "affirmation": None,
                                  "num_affirmations": None,
                                  "supporting_arguments": None,
                                  "supported_arguments": None,
                                  })
    claim_obj = Claim.objects.get(pk=claim)
    context["vue_claims"][0]["claim"] = claim_obj
    try:
        affirmation_obj = Affirmation.objects.get(claim_id=claim,
                                                  user_id=request.user)
        context["vue_claims"][0]["affirmation"] = affirmation_obj
    except Affirmation.DoesNotExist:
        pass
    num_affirmations = Affirmation.objects.filter(claim_id=claim).count()
    context["vue_claims"][0]["num_affirmations"] = num_affirmations
    supporting_arguments = Argument.objects.filter(supported_claim_id=claim)
    context["vue_claims"][0]["supporting_arguments"] = supporting_arguments
    print(context)

    return render(request, "claims/claim_single.html", context)


# View Argument
def ArgumentView(request, argument):
    context = {}

    try:
        this_argument = Argument.objects.get(pk=argument)
    except Argument.DoesNotExist:
        raise Http404("Argument does not exist")

    context["argument"] = this_argument

    return render(request, "claims/viewArgument.html", context)


# View Recommendations
@login_required
def recommendations(request):
    context = {}

    # get list of recommended claims
    rl = fcns.getClaimRecommendations(request.user)
    rl_concls = filter(lambda x: x['rec_type'] == 'conclusion', rl)
    rl_concl_ids = [rl_concls[a][0] for a in range(len(rl_concls))]
    rl_concl_claims = Claim.objects.filter(pk__in=rl_concl_ids)
    context["recommended_conclusions"] = rl_concl_claims

    # get list of recommended claims
    rl = getClaimRecommendations(request.user)
    rl_premises = filter(lambda x: x['rec_type'] == 'premise', rl)
    rl_premise_ids = [rl_premises[a][0] for a in range(len(rl_premises))]
    rl_premise_claims = Claim.objects.filter(pk__in=rl_premise_ids)
    context["recommended_premises"] = rl_premise_claims

    return render(request, "claims/recommendations.html", context)


# List all Claims
# class ClaimListView(ListView):
#     model = Claim


# View Claim
def ClaimListView(request):

    if request.user.is_authenticated():
        fcns.sync_graph(user=request.user)

    context = {}

    # building context varianle for vue.js
    context["vue_claims"] = []

    for i, claim in enumerate(Claim.objects.all()):
        context["vue_claims"].append({"claim": None,
                                      "affirmation": None,
                                      "num_affirmations": None,
                                      "supporting_arguments": None,
                                      "supported_arguments": None,
                                      })
        claim_obj = claim
        context["vue_claims"][i]["claim"] = claim_obj
        try:
            affirmation_obj = Affirmation.objects.get(claim_id=claim,
                                                      user_id=request.user)
            context["vue_claims"][i]["affirmation"] = affirmation_obj
        except Affirmation.DoesNotExist:
            pass
        num_affirmations = Affirmation.objects.filter(claim_id=claim).count()
        context["vue_claims"][i]["num_affirmations"] = num_affirmations
        supporting_arguments = Argument.objects.filter(supported_claim_id=claim)
        context["vue_claims"][i]["supporting_arguments"] = supporting_arguments
        print(context)

    return render(request, "claims/claim_single.html", context)



# List all Arguments
class ArgumentListView(ListView):
    model = Argument


# API Views

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

            fcns.addAffirmationToGraph(affirmation)

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
        fcns.removeAffirmationFromGraph(affirmation)
        affirmation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
