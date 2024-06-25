import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from gptlawyer import models


class UserType(DjangoObjectType):
    class Meta:
        model = models.User

class StudyCaseType(DjangoObjectType):
    class Meta:
        model = models.StudyCase

    number_of_collaborators = graphene.Int(source="get_number_of_collaborators")

    def resolve_number_of_collaborators(self, info):
        return self.get_number_of_collaborators()

class MessageType(DjangoObjectType):
    class Meta:
        model = models.Message
        
class StudyCaseInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()


class UpdateStudyCaseInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    title = graphene.String()
    description = graphene.String()


class CollaboratorType(DjangoObjectType):
    class Meta:
        model = models.Collaborator

class CollaboratorInput(graphene.InputObjectType):
    user_id = graphene.ID(required=True)
    study_case_id = graphene.ID(required=True)
    #role_id = graphene.ID(required=True)

class UpdateCollaboratorInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    user_id = graphene.ID()
    study_case_id = graphene.ID()
    #role_id = graphene.ID()


""" class RoleType(DjangoObjectType):
    class Meta:
        model = models.Role

class RoleInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class UpdateRoleInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String() """

class DocumentType(DjangoObjectType):
    class Meta:
        model = models.Document


class DocumentInput(graphene.InputObjectType):
    file = Upload(required=True)
    study_case_id = graphene.ID(required=True)

class UpdateDocumentInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    content = graphene.String()

