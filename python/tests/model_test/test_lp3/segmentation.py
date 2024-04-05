import os
import cv2
import numpy as np
import mediapipe as mp

# 입력 폴더 경로
input_folder_path = './input/'
# 출력 폴더 경로
output_folder_path = './output/'

# 모델 생성
with mp.solutions.hair_segmentation.HairSegmentation(model_selection=1) as model:

    # 입력 폴더 내의 이미지 파일들에 대해 처리
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_folder_path, filename)
            # 이미지 불러오기
            image = cv2.imread(image_path)
            # BGR을 RGB로 변환
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # 세그멘테이션 수행
            results = model.process(image_rgb)
            mask = results.segmentation_mask

            # 출력 이미지 생성
            output_image = np.zeros(image.shape, dtype=np.uint8)
            output_image[:, :] = (192, 192, 192)  # 회색 배경

            # 마스크 기반으로 출력 이미지 생성
            condition = mask > 0.2
            output_image = np.where(np.expand_dims(condition, axis=-1), image, output_image)

            # 출력 이미지 저장
            output_image_path = os.path.join(output_folder_path, filename.split('.')[0] + '_output.jpg')
            cv2.imwrite(output_image_path, output_image)
