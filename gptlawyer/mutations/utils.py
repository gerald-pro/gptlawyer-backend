import string
import PyPDF2
import easyocr
from docx import Document
from django.db.models.fields.files import FieldFile


def extract_from_image(file: FieldFile):
    reader = easyocr.Reader(["es"], gpu=True)
    result = reader.readtext(file.path, detail=0, paragraph=True)
    contenido_imagen = " ".join(result)
    return contenido_imagen


def extract_from_pdf(file: FieldFile):
    contenido_pdf = ""
    reader = PyPDF2.PdfReader(file)
    for pagina in range(len(reader.pages)):
        contenido_pdf += reader.pages[pagina].extract_text()
    return contenido_pdf


def extract_from_word(file: FieldFile):
    documento_word = Document(file)
    contenido_word = "\n".join([para.text for para in documento_word.paragraphs])
    return contenido_word


def extract_text(content_type: string, file: FieldFile):
    contenido = ""
    if content_type == "image/jpeg" or content_type == "image/png":
        contenido = extract_from_image(file)
    if content_type == "application/pdf":
        contenido = extract_from_pdf(file)
    elif (
        content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        contenido = extract_from_word(file)
    return contenido
