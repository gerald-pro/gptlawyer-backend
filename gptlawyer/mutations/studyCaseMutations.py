import graphene
from gptlawyer import types
from gptlawyer import models
from graphql_jwt.decorators import login_required


class CreateStudyCase(graphene.Mutation):
    study_case = graphene.Field(types.StudyCaseType)

    class Arguments:
        input = types.StudyCaseInput()

    @staticmethod
    @login_required
    def mutate(root, info, input):
        user = info.context.user

        study_case_instance = models.StudyCase(
            title=input.title, description=input.description, owner=user
        )
        study_case_instance.save()
        return CreateStudyCase(study_case=study_case_instance)


class UpdateStudyCase(graphene.Mutation):
    class Arguments:
        input = types.UpdateStudyCaseInput(required=True)

    study_case = graphene.Field(types.StudyCaseType)

    @staticmethod
    @login_required
    def mutate(root, info, input):

        study_case_instance = models.StudyCase.objects.get(pk=input.id)
        if study_case_instance:
            if input.title:
                study_case_instance.title = input.title
            if input.description:
                study_case_instance.description = input.description

            study_case_instance.save()
            return UpdateStudyCase(study_case=study_case_instance)
        return UpdateStudyCase(study_case=None)


class DeleteStudyCase(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, id):
        study_case_instance = models.StudyCase.objects.get(pk=id)
        if study_case_instance:
            study_case_instance.delete()
            return DeleteStudyCase(success=True)
        return DeleteStudyCase(success=False)


class StudyCaseMutations(graphene.ObjectType):
    create_study_case = CreateStudyCase.Field()
    update_study_case = UpdateStudyCase.Field()
    delete_study_case = DeleteStudyCase.Field()
