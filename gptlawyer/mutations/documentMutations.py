import graphene
from gptlawyer import types
from gptlawyer import models
from graphql_jwt.decorators import login_required
from gptlawyer.mutations.utils import extract_text
from django.db import transaction

class UploadDocument(graphene.Mutation):
    class Arguments:
        input = types.DocumentInput(required=True)

    document = graphene.Field(types.DocumentType)

    @login_required
    @transaction.atomic
    def mutate(self, info, input):
        user = info.context.user
        study_case = models.StudyCase.objects.get(id=input.study_case_id)

        document_instance = models.Document(
            name=input.file.name,
            content_type=input.file.content_type,
            study_case=study_case,
            uploaded_by=user,
            file=input.file,
        )

        document_instance.save()

        extracted_text = extract_text(
            document_instance.content_type, document_instance.file
        )
        document_instance.content = extracted_text

        document_instance.save()

        return UploadDocument(document=document_instance)


class UpdateDocument(graphene.Mutation):
    class Arguments:
        input = types.UpdateDocumentInput(required=True)

    document = graphene.Field(types.DocumentType)

    @staticmethod
    @login_required
    def mutate(root, info, input: types.UpdateDocumentInput):

        doc_instance = models.Document.objects.get(pk=input.id)
        if doc_instance:
            if input.name:
                doc_instance.name = input.name
            if input.content:
                doc_instance.content = input.content

            doc_instance.save()
            return UpdateDocument(document=doc_instance)
        return UpdateDocument(studdocumenty_case=None)


class DeleteDocument(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, id):
        doc_instance = models.Document.objects.get(pk=id)
        if doc_instance:
            doc_instance.delete()
            return DeleteDocument(success=True)
        return DeleteDocument(success=False)


class DocumentMutations(graphene.ObjectType):
    upload_document = UploadDocument.Field()
    update_document = UpdateDocument.Field()
    delete_document = DeleteDocument.Field()
