import json
from flask import Flask
from flask_graphql import GraphQLView
import graphene

# Load data from local JSON file
with open('data.json') as f:
    user_data = json.load(f)

# GraphQL Types
class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

# Query Resolver
class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_users(self, info):
        return user_data

    def resolve_user(self, info, id):
        return next((u for u in user_data if u["id"] == id), None)

# Schema
schema = graphene.Schema(query=Query)

# Flask App
app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
