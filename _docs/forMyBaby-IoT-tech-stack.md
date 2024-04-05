[AI - vision 1. Media-Pipe : TensorFlow Lite를 기반 On-device ML]
    main-func 1. 영상 인식 기반 위험 행동 감지
        (b) pose detection
            ex 1. 뒤집기 
        (c) face detection
            ex 1. 얼굴이 감지 안된다
        (+) 딥러닝 기반 위험 행동 감지 (뒤집기, 추락 등)
            - 데이터 : 관성 센서
            - 모델 : CNN,LSTM ...
        
    main-func 2. 영상 인식 기반 수면 감지를 통한 아이 수면 패턴 분석 및 시각화
        (a) baby - Image segmentation (multi class selfie segmenter 활용)
            ex 1. 카메라에 피부가 감지가 안된다.
        (b) pose detection (moving)
            ex 1. 움직임이 다수 발생
        (c) face detection
            ex 1. 얼굴이 감지 안된다
            ex 2. 눈코입이 감지 안된다
        (+) 관성 센서 데이터 활용을 통한 움직인 거리 등 다양한 특성 시각화


    main-func 3. 동작 감지를 통한 성장 스탬프
        (b) pose detection (CNN(Convolutional Neural Network)기반)
        (a) localization - Image segmentation (multi class selfie segmenter 활용)
            - 영역을 벗어나면 감지

    main-func 4. 영역 및 동작 인식을 통해 촬영된 사진 기반 스톱 모션 제작
        (a) localization - Image segmentation (multi class selfie segmenter 활용)
            - 영역을 벗어나면 감지

[AI - vision 2. OpenPose : VGG-19 백본이 있는 ImageNet기반 동작의 특징점(관절)을 추출]
    Media-pipe의 pose detection 에 대한 대안으로 활용 예정

[Extra - 온습도 Sensor]
    sub-func 1. 실내 적정 온습도 유지를 위한 실시간 온습도 측정 및 시각화





    - 비전 
        - 이미지와 비디오에 있는 내용 분석
        - object detection
        - pose detection
        - face detection
        - Image segmentation
            1. 
                MVP 구현
            2. multi class selfie segmenter 
                - Image coverage: background / hair / face-skin / clothes / body-skin
                - hair segmenter 참조
