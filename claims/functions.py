from django.conf import settings
from claims.models import ArgumentPremise
# Neo4J
from py2neo import authenticate, Graph, Node, Relationship
# for sync_graph
from claims.models import Claim, Argument, Affirmation
from django.contrib.auth.models import User


# Claims
def addClaimToGraph(claim):
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    tx = graph.begin()
    claimNode = Node("Claim",
                     claim_id=claim.id,
                     name=claim.name,
                     content=claim.content)
    tx.merge(claimNode, 'claim_id')
    tx.commit()


# Users
def addUserToGraph(user):
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    tx = graph.begin()
    userNode = Node("User", user_id=user.id, name=user.username)
    tx.merge(userNode, 'user_id')
    tx.commit()


def addArgumentToGraph(argument):
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    tx = graph.begin()
    argumentNode = Node("Argument", argument_id=argument.id, name=argument.name)
    tx.merge(argumentNode, 'argument_id')
    for p in ArgumentPremise.objects.filter(argument_id=argument.id):
        premiseClaim = p.claim
        premiseClaimNode = Node("Claim",
                                claim_id=premiseClaim.id,
                                name=premiseClaim.name,
                                content=premiseClaim.content)
        tx.merge(premiseClaimNode, 'claim_id')
        premiseOfRelationship = Relationship(premiseClaimNode,
                                             "Premise_Of",
                                             argumentNode,
                                             argumentpremise_id=p.id)
        tx.merge(premiseOfRelationship, 'argumentpremise_id')
    supportedClaim = argument.supported_claim
    supportedClaimNode = Node("Claim",
                              claim_id=supportedClaim.id,
                              name=supportedClaim.name,
                              content=supportedClaim.content)
    tx.merge(supportedClaimNode, 'claim_id')
    supportsRelationship = Relationship(argumentNode,
                                        "Supports",
                                        supportedClaimNode,
                                        argument_id=argument.id)
    tx.merge(supportsRelationship, 'argument_id')
    tx.commit()


# Affirmations
def addAffirmationToGraph(affirmation):
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    tx = graph.begin()
    claim = affirmation.claim
    claimNode = Node("Claim",
                     claim_id=claim.id,
                     name=claim.name,
                     content=claim.content)
    tx.merge(claimNode, 'claim_id')
    user = affirmation.user
    userNode = Node("User",
                    user_id=user.id,
                    name=user.username)
    tx.merge(userNode, 'user_id')
    affirmsRelationship = Relationship(userNode,
                                       "Affirms",
                                       claimNode,
                                       affirmation_id=affirmation.id)
    tx.merge(affirmsRelationship, 'affirmation_id')
    tx.commit()


def removeAffirmationFromGraph(affirmation):
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    tx = graph.begin()
    claim = affirmation.claim
    claimNode = Node("Claim",
                     claim_id=claim.id,
                     name=claim.name,
                     content=claim.content)
    tx.merge(claimNode, 'claim_id')
    user = affirmation.user
    userNode = Node("User",
                    user_id=user.id,
                    name=user.username)
    tx.merge(userNode, 'user_id')
    affirmsRelationship = Relationship(userNode,
                                       "Affirms",
                                       claimNode,
                                       affirmation_id=affirmation.id)
    tx.merge(affirmsRelationship, 'affirmation_id')
    tx.separate(affirmsRelationship)
    tx.commit()


def sync_graph(user):

    # delete the graph
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    graph.run('MATCH (n) DETACH DELETE n')

    for c in Claim.objects.all():
        # print(c)
        addClaimToGraph(claim=c)

    for u in User.objects.all():
        # print(u)
        addUserToGraph(user=u)

    for arg in Argument.objects.all():
        # print(arg)
        addArgumentToGraph(argument=arg)

    for aff in Affirmation.objects.all():
        # print(aff)
        addAffirmationToGraph(affirmation=aff)
