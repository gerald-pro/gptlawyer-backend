import graphene
from .studyCaseMutations import StudyCaseMutations
from .collaboratorMutations import CollaboratorMutations
from .documentMutations import DocumentMutations
from .userMutations import UserMutations


class Mutation(UserMutations, StudyCaseMutations, CollaboratorMutations, DocumentMutations, graphene.ObjectType):
    pass
