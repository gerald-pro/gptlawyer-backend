import os
import string
import PyPDF2
import cv2
import easyocr
from docx import Document
from django.db.models.fields.files import FieldFile


def extract_from_image(file: FieldFile):
    file_path = file.path

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"El archivo {file_path} no tiene permisos de lectura.")
    
    if os.stat(file_path).st_size == 0:
        raise ValueError(f"El archivo {file_path} está vacío.")
    
    try:
        # Preprocesar la imagen
        processed_image = preprocess_image(file_path)

        temp_file_path = file_path + "_processed.png"
        cv2.imwrite(temp_file_path, processed_image)

        reader = easyocr.Reader(["es"], gpu=False)
        result = reader.readtext(temp_file_path, detail=0, paragraph=True)
        

        contenido_imagen = " ".join(result)
        return contenido_imagen
    except Exception as e:
        raise RuntimeError(f"Error al procesar la imagen: {str(e)}")


def preprocess_image(file_path):
    image = cv2.imread(file_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    denoised = cv2.fastNlMeansDenoising(gray, None, h=3, searchWindowSize=21, templateWindowSize=7)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4,4))
    contrast_enhanced = clahe.apply(denoised)
    return contrast_enhanced


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
