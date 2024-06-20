"""
Defina el esquema GraphQL para la aplicación.

Este esquema se basa en la clase `Query` del módulo `gptlawyer.queries`,
que contiene las definiciones de las consultas GraphQL disponibles.
"""

import graphene
from gptlawyer import queries
from .mutations import Mutation

schema = graphene.Schema(query=queries.Query, mutation=Mutation)