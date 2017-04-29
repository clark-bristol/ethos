from django.conf import settings
from claims.models import ArgumentPremise
# Neo4J
from py2neo import authenticate, Graph, Node, Relationship
# for sync_graph
from claims.models import Claim, Argument, Affirmation
from django.contrib.auth.models import User

# Prepare data for Vue.js
def addClaimInfoToContextForVue(context, user, claim, i):
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
                                                  user_id=user)
        context["vue_claims"][i]["affirmation"] = affirmation_obj
    except Affirmation.DoesNotExist:
        pass
    num_affirmations = Affirmation.objects.filter(claim_id=claim).count()
    context["vue_claims"][i]["num_affirmations"] = num_affirmations
    supporting_arguments = Argument.objects.filter(supported_claim_id=claim)
    context["vue_claims"][i]["supporting_arguments"] = supporting_arguments
    return context

# Recommendations
def getClaimRecommendations(user):
    # delete the graph
    authenticate(settings.SECRET_NEO4J_DB_HOSTPORT,
                 settings.SECRET_NEO4J_DB_USER,
                 settings.SECRET_NEO4J_DB_PASSWORD)
    graph = Graph()
    query_conclusions = '''
        // get all arguments supported by claims affirmed by the user
        MATCH (u:User {user_id:%s})-[:Affirms]->(sc1:Claim)-[:Premise_Of]->(a:Argument)-[:Supports]->(cc:Claim)
            , (sc:Claim)-[:Premise_Of]->(a) // get all supporting claims of those arguments
        WHERE NOT (u)-[:Affirms]->(cc) // where the user does not already affirm the argument's conclusion
        WITH u, a, cc, COLLECT(sc) AS supporting_claims
        WHERE ALL (sc IN supporting_claims WHERE (u)-[:Affirms]->(sc)) // where the user affirms all supporting claims of the argument
        RETURN cc.claim_id AS claim_id, 'conclusion' AS rec_type
        ''' % (user.id)

    rec_list = list(graph.run(query_conclusions))

    query_premises = '''
        // get all arguments supported by claims affirmed by the user
        MATCH (u:User {user_id:%s})-[:Affirms]->(sc1:Claim)-[:Premise_Of]->(a:Argument)-[:Supports]->(cc:Claim)
            // get all supporting claims of those arguments
            , (sc:Claim)-[:Premise_Of]->(a)
        // where the user does affirm the argument's conclusion
        WHERE (u)-[:Affirms]->(cc)
        // return the premises that the user does not yet affirm
        WITH u, a, cc, sc
        WHERE NOT (u)-[:Affirms]->(sc)
        RETURN sc.claim_id AS claim_id, 'premise' AS rec_type
        ''' % (user.id)

    # get query results as a list of named tuples
    rec_list += list(graph.run(query_premises))

    return rec_list


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
    argumentNode = Node("Argument",
                        argument_id=argument.id,
                        name=argument.name)
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

    # getClaimRecommendations(user)
