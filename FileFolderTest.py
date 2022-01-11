import unittest
import pathlib
import shutil
import os
import AIAgeGenderAPI as AI
import IdentifyImageService as service

class MyTestCase(unittest.TestCase):

    def test_identify_image_serial(self):
        service.IdentifyImage("./resources/faces-dataset", "./resources/faces-female",
                              "./resources/faces-male", max_files_count=50).serial()

    def test_ai_api(self):
        AI.analysisImage("./resources/faces-dataset/00001.png")

    def test_move_file(self):
        os.rename('./resources/faces-dataset/00023.png', './resources/faces-male/00023.png')

    def test_move_folder(self):
        faces = pathlib.Path("./resources/faces-male")
        for face in faces.iterdir():
            os.remove(str(face))

    def test_copy_file(self):
        shutil.copyfile('./resources/faces-dataset/00023.png', './resources/faces-male/00023.png')

    def test_del_file(self):
        os.remove('./resources/faces-male/00023.png')

    def test_path(self):
        faces = pathlib.Path("./resources/faces-dataset")
        for face in faces.iterdir():
            print(face)

    def test_parse_file_name(self):
        str = "./resources/faces-dataset/00001.png"
        print(str.split("/")[-1])
        print(str + "/test/test2")


if __name__ == '__main__':
    unittest.main()
