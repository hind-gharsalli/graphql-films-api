import strawberry
from fastapi import FastAPI, Depends, Request, HTTPException
from strawberry.fastapi import GraphQLRouter
from database import get_db, init_db
from queries import Query
from mutations import Mutation
from subscriptions import Subscription
from auth import verify_token

# 1. Créer le schéma GraphQL complet
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

# 2. Le SEUL et UNIQUE get_context (Base de données + Sécurité)
async def get_context(request: Request, db=Depends(get_db)):
    # Récupérer le token depuis l'en-tête Authorization
    auth_header = request.headers.get("Authorization", "")
    user = None
    
    if auth_header.startswith("Bearer "):
        try:
            user = verify_token(auth_header.split(" ")[1])
        except Exception:
            raise HTTPException(status_code=401, detail="Token invalide")
            
    return {"db": db, "user": user}

# 3. Créer l'application GraphQL AVEC le bon contexte
graphql_app = GraphQLRouter(schema, context_getter=get_context)

# 4. Initialiser FastAPI
app = FastAPI(title="API GraphQL Films")
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("startup")
def startup():
    init_db()

# Lancer avec : uvicorn main:app --reload
