# Import required modules
import time
import cv2 as cv
import shutil
import logging
import pathlib
import os
'''
@Author by Liu Jiage
@Date 1th June 2021
@Function output the function running logs for testing
'''
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [*] %(processName)s %(threadName)s %(message)s"
)

'''
@Author by Liu Jiage
@Date 5th June 2021
@Function extra face from image
@Source from OpenCV one example
'''

def getFaceBox(net, frame, conf_threshold=0.7, high=128, width=128):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (high, width), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, bboxes


'''
@Author by Liu Jiage
@Date 5th June 2021
@Function Analysis image
@Source from OpenCV one example 
@Param _fileName is an image path 
@Param _result saving all analysis results.
@Param _model=copy default is None. doing nothing. 
'''

def analysisImage(_fileName, _result=[], _model=None):

    faceProto = "../resources/opencv/opencv_face_detector.pbtxt"
    faceModel = "../resources/opencv/opencv_face_detector_uint8.pb"
    ageProto = "../resources/opencv/age_deploy.prototxt"
    ageModel = "../resources/opencv/age_net.caffemodel"
    genderProto = "../resources/opencv/gender_deploy.prototxt"
    genderModel = "../resources/opencv/gender_net.caffemodel"
    maleFolder = "../resources/faces-male"
    femaleFolder = "../resources/faces-female"
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']
    # Load network
    ageNet = cv.dnn.readNet(ageModel, ageProto)
    genderNet = cv.dnn.readNet(genderModel, genderProto)
    faceNet = cv.dnn.readNet(faceModel, faceProto)
    ageNet.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
    genderNet.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
    faceNet.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
    _fileName = str(_fileName)
    im = cv.imread(_fileName)
    _high, _width, c = im.shape
    _high = int(_high - (_high * 0.5))
    _width = int(_width - (_width * 0.5))
    # Open a video file or an image file or a camera stream
    cap = cv.VideoCapture(_fileName if _fileName else 0)
    padding = 20
    # print(_fileName)
    # Read frame
    startTime = time.time()
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        print("No face Detected,file name: ", _fileName)
        return
    frameFace, bboxes = getFaceBox(faceNet, frame, high=_high, width=_width)
    if not bboxes:
        print("No face Detected,file name: ", _fileName)
        return
    gender = None
    for bbox in bboxes:
        face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
               max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
        blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        label = "{},{}".format(gender, age)
    # print analysis information detail
    logging.info("time:{:.3f} result:{} fileName:{}".format(
        time.time() - startTime, label, _fileName))
    # copy image to different folder male or female
    if _model is not None and _model == 'copy':
        if gender is None:
            return label
        elif gender == 'Male':
            shutil.copyfile(_fileName, maleFolder + "/" + _fileName.split("/")[-1])
        elif gender == 'Female':
            shutil.copyfile(_fileName, femaleFolder + "/" + _fileName.split("/")[-1])
    # save the result
    _result.append(label)
    return label