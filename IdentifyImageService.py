import pathlib
import time
import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from joblib import Parallel, delayed

import AIAgeGenderAPI as AI

'''
@Author by Liu Jiage
@Date 1th June 2021
@Describe
First, load a image folder
And then, identify their gender and age
Finally, move the image into different folders male or female.
'''
class IdentifyImage(object):

    '''
        @Function init parameters
        @param image_folder_path is going to load a images folder
        @param female_folder_path is going to save female images
        @param male_folder_path is going to save male images
        @param max_files_count is the maximum number of pictures processed
    '''

    def __init__(self, image_folder_path, female_folder_path,
                 male_folder_path, max_files_count=50, ai_model=None):
        self._image_folder_path = image_folder_path
        self._female_folder_path = female_folder_path
        self._male_folder_path = male_folder_path
        self._max_files_count = max_files_count
        self._result = []
        self._ai_model = ai_model
        self._model = "serial"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [*] %(processName)s %(threadName)s %(message)s"
        )

    '''
    @Author by Liu Jiage
    @Function serial processing tasks
    '''
    def serial(self):
        self._model = "serial"
        self.parallel(amount=1)

    '''
    @Author by Liu Jiage
    @Function parallel processing tasks 
    @Param model 'threading','multiprocessing','loky'; default = 'threading'
    @Param amount default = 5
    @param debugLevel default = 10. Debug level 10~50
    '''

    def parallel(self, model="threading", amount=2, debugLevel=0):
        self._model = "parallel"
        # empty temp folders if _model=copy
        self.clearFolder([self._female_folder_path, self._male_folder_path])
        startTime = time.time()
        self._result = []
        # 1) load images from image folder
        images = self._getImages()
        # 2) analysis image. Using joblib API
        Parallel(n_jobs=amount, verbose=debugLevel, backend=model)(
            delayed(AI.analysisImage)(n, _model=self._ai_model) for n in images[0:self._max_files_count])
        # 3) output the result
        print("Finally report record - Total time:{:.3f}sec Total count:{}; Model:{} Parallel amount: {}".format(
                time.time() - startTime, len(images), self._model, amount))

    '''
    @Author by Liu Jiage
    @Function get images. 
    '''

    def _getImages(self):
        # 1) load images from image folder
        faces = pathlib.Path(self._image_folder_path)
        list = []
        totalCount = 0
        for face in faces.iterdir():
            if totalCount >= self._max_files_count:
                break
            list.append(face)
            totalCount += 1
        return list

    '''
    @Author by Liu Jiage
    @Function empty folders
    '''
    @staticmethod
    def clearFolder(folders=None):
        if folders is None:
            return
        for folder in folders:
            faces = pathlib.Path(folder)
            for face in faces.iterdir():
                os.remove(str(face))
