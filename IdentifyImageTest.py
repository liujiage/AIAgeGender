import unittest
import IdentifyImageService as service
'''
@Author Liu Jiage
@Date 2th June 2021
'''
class MyTestCase(unittest.TestCase):

    '''
       @Function serial processing tasks
       @Test
          100 images 22.315sec
          200 images 44.201sec
          300 images 65.232sec
    '''
    def test_identify_image_serial(self):
        service.IdentifyImage("./resources/faces-dataset", "./resources/faces-female",
                              "./resources/faces-male", max_files_count=100, ai_model='copy').serial()

    '''
       @Function parallel processing tasks 
       @Param type 'threading','multiprocessing','loky'; default = 'threading'
       @Param amount default = 5
       @param debugLevel default = 10. Debug level 10~50
       @Test 
          100 images threading(5) 11.692sec, multiprocessing(5) 12.631sec
          200 images threading(5) 23.543sec, multiprocessing(5) 23.634sec
          300 images threading(5) 34.515sec, multiprocessing(5) 33.933sec
    '''
    def test_identify_image_parallel(self):
        service.IdentifyImage("./resources/faces-dataset", "./resources/faces-female",
                              "./resources/faces-male", max_files_count=500, ai_model='copy').parallel(model="multiprocessing", amount=5)

    '''
       @Function clear folder 
    '''
    def test_clear_folder(self):
        service.IdentifyImage.clearFolder(["./resources/faces-female", "./resources/faces-male"])

if __name__ == '__main__':
    unittest.main()
