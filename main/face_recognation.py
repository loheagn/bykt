import dlib
import numpy as np
import cv2
import os
import json


# 获取某人的特征向量的二维矩阵
def get_src_vectors_from_someone_images(image_path):
    data = np.zeros((1, 128))  # 定义一个128维的空向量data
    label = []  # 定义空的list存放人脸的标签
    detector = dlib.cnn_face_detection_model_v1('mmod')
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

    for file_name in os.listdir(image_path):
        img = cv2.imread(image_path + file_name)  # 使用opencv读取图像数据
        dets = detector(img, 1)  # 使用检测算子检测人脸，返回的是所有的检测到的人脸区域
        for k, d in enumerate(dets):
            rec = dlib.rectangle(d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom())
            shape = sp(img, rec)  # 获取landmark
            face_descriptor = facerec.compute_face_descriptor(img, shape)  # 使用resNet获取128维的人脸特征向量
            faceArray = np.array(face_descriptor).reshape((1, 128))  # 转换成numpy中的数据结构
            data = np.concatenate((data, faceArray))  # 拼接到事先准备好的data当中去
            label.append(label)  # 保存标签
            cv2.rectangle(img, (rec.left(), rec.top()), (rec.right(), rec.bottom()), (0, 255, 0), 2)  # 显示人脸区域
        cv2.waitKey(2)
        cv2.imshow('image', img)
    cv2.destroyAllWindows()  # 关闭所有窗口
    return data[1:, :]


def get_src_vectors_from_someone_single_image(file_name):
    data = np.zeros((1, 128))  # 定义一个128维的空向量data
    label = []  # 定义空的list存放人脸的标签
    detector = dlib.cnn_face_detection_model_v1('/home/loheagn/boyasite/main/mmod_human_face_detector.dat')
    sp = dlib.shape_predictor('/home/loheagn/boyasite/main/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('/home/loheagn/boyasite/main/dlib_face_recognition_resnet_model_v1.dat')

    img = cv2.imread(file_name)  # 使用opencv读取图像数据
    dets = detector(img, 1)  # 使用检测算子检测人脸，返回的是所有的检测到的人脸区域
    for k, d in enumerate(dets):
        rec = dlib.rectangle(d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom())
        shape = sp(img, rec)  # 获取landmark
        face_descriptor = facerec.compute_face_descriptor(img, shape)  # 使用resNet获取128维的人脸特征向量
        faceArray = np.array(face_descriptor).reshape((1, 128))  # 转换成numpy中的数据结构
        data = np.concatenate((data, faceArray))  # 拼接到事先准备好的data当中去
        label.append(label)  # 保存标签
        cv2.rectangle(img, (rec.left(), rec.top()), (rec.right(), rec.bottom()), (0, 255, 0), 2)  # 显示人脸区域
    cv2.waitKey(2)
    cv2.imshow('image', img)
    cv2.destroyAllWindows()  # 关闭所有窗口
    return data[1:, :]


def get_dst_vectors_from_single_image(file_name):
    data = np.zeros((1, 128))  # 定义一个128维的空向量data
    label = []  # 定义空的list存放人脸的标签
    detector = dlib.cnn_face_detection_model_v1('/home/loheagn/boyasite/main/mmod_human_face_detector.dat')
    sp = dlib.shape_predictor('/home/loheagn/boyasite/main/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('/home/loheagn/boyasite/main/dlib_face_recognition_resnet_model_v1.dat')
    img = cv2.imread(file_name)  # 使用opencv读取图像数据
    dets = detector(img, 1)  # 使用检测算子检测人脸，返回的是所有的检测到的人脸区域

    for k, d in enumerate(dets):
        rec = dlib.rectangle(d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom())
        shape = sp(img, rec)  # 获取landmark
        face_descriptor = facerec.compute_face_descriptor(img, shape)  # 使用resNet获取128维的人脸特征向量
        faceArray = np.array(face_descriptor).reshape((1, 128))  # 转换成numpy中的数据结构
        data = np.concatenate((data, faceArray))  # 拼接到事先准备好的data当中去
        label.append(label)  # 保存标签
        cv2.rectangle(img, (rec.left(), rec.top()), (rec.right(), rec.bottom()), (0, 255, 0), 2)  # 显示人脸区域
    cv2.waitKey(2)
    cv2.imshow('image', img)
    cv2.destroyAllWindows()
    return data[1:, :]


if __name__ == "__main__":
    src_data = get_src_vectors_from_someone_images("./img/src/",)
    dst_data = get_dst_vectors_from_single_image("./img/test/", "7a939b9d9b9824de33d85e65ba119693.jpg")

    st = src_data.tostring()

    src_data2 = np.fromstring(st)
    temp = dst_data - src_data
    e = np.linalg.norm(temp, axis=1, keepdims=True)
    min_distance = e.min()
    print('distance: ', min_distance)

    temp = dst_data - src_data2
    e = np.linalg.norm(temp, axis=1, keepdims=True)
    min_distance = e.min()
    print('distance: ', min_distance)
