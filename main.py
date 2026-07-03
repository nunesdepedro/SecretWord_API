from fastapi import FastAPI

from app.core.database import Base
from app.routes.passwords_routes import passwords_routes
from app.routes.auth_routes import auth_router
from app.core.database import db

# # Esta linha cria as tabelas se elas não existirem
# Base.metadata.create_all(bind=db)

app = FastAPI(title="SecretWord API")

app.include_router(auth_router)
app.include_router(passwords_routes)



# from fastapi.openapi.utils import get_openapi

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title="SecretWord API",
#         version="1.0.0",
#         description="API com JWT auth",
#         routes=app.routes,
#     )

#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT"
#         }
#     }

#     # aplica auth global no swagger
#     for path in openapi_schema["paths"]:
#         for method in openapi_schema["paths"][path]:
#             openapi_schema["paths"][path][method]["security"] = [
#                 {"BearerAuth": []}
#             ]

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi