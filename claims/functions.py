from django.conf import settings
from claims.models import ArgumentPremise
# Neo4J
from py2neo import authenticate, Graph, Node, Relationship
# List view

#
# Webpage Views
#


# Add Claim to Graph
def addClaimAndUserToGraph(claim, user):

    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT, settings.SECRET_NEO4J_DB_USER, settings.SECRET_NEO4J_DB_PASSWORD)
    claimNode = Node("Claim", claim_id=claim.id, name=claim.name, content=claim.content)
    userNode = Node("User", user_id=user.id, name=user.username)
    subgraph = claimNode | userNode
    graph = Graph()
    tx = graph.begin()
    tx.merge(subgraph, primary_label='name')
    tx.commit()


# Add Argument to Graph
def addArgumentToGraph(argument, user):

    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT, settings.SECRET_NEO4J_DB_USER, settings.SECRET_NEO4J_DB_PASSWORD)
    argumentNode = Node("Argument", argument_id=argument.id, name=argument.name)
    subgraph = argumentNode

    for argumentPremise in ArgumentPremise.objects.filter(argument_id=argument.id):
        premiseClaim = argumentPremise.claim
        premiseClaimNode = Node("Claim", claim_id=premiseClaim.id, name=premiseClaim.name, content=premiseClaim.content)
        premiseOfRelationship = Relationship(premiseClaimNode, "Premise_Of", argumentNode)
        subgraph = subgraph | premiseClaimNode | premiseOfRelationship

    supportedClaim = argument.supported_claim
    supportedClaimNode = Node("Claim", claim_id=supportedClaim.id, name=supportedClaim.name, content=supportedClaim.content)
    supportsRelationship = Relationship(argumentNode, "Supports", supportedClaimNode)
    subgraph = subgraph | supportedClaimNode | supportsRelationship

    graph = Graph()
    tx = graph.begin()
    tx.merge(subgraph, primary_label='name')
    tx.commit()


# Add Affirmation to Graph
def addAffirmationToGraph(claim, user):

    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT, settings.SECRET_NEO4J_DB_USER, settings.SECRET_NEO4J_DB_PASSWORD)
    claimNode = Node("Claim", claim_id=claim.id, name=claim.name, content=claim.content)
    userNode = Node("User", user_id=user.id, name=user.username)
    affirmsRelationship = Relationship(userNode, "Affirms", claimNode)
    subgraph = claimNode | userNode | affirmsRelationship
    graph = Graph()
    tx = graph.begin()
    tx.merge(subgraph, primary_label='name')
    tx.commit()
