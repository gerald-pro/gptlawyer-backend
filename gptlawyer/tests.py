import os
import cv2
import matplotlib.pyplot as plt
from django.test import TestCase
from gptlawyer.mutations.utils import extract_from_image, preprocess_image


class DetectionTestCase(TestCase):
    def test_detection_method(self):
        test_dir = os.path.dirname(__file__)
        test_image_path = os.path.join(
            test_dir, "documents/example.jpg"
        )

        print(test_image_path)

        if not os.path.exists(test_image_path):
            print(f"El archivo {test_image_path} no existe.")
        else:
            processed_image = preprocess_image(test_image_path)

            plt.imshow(cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB))
            plt.title('Imagen Preprocesada')
            plt.show()

            #cv2.imwrite('imagen_preprocesada.png', processed_image)