"""
GraphQL API URLs
"""

from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from api.graphql.schema import schema


urlpatterns = [
    # GraphQL endpoint
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='graphql'),

    # GraphQL Playground (development only)
    path('graphql/playground/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='graphql-playground'),
]
