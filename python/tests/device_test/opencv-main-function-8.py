import matplotlib.pyplot as plt
import cv2
 
#컬러 영상 출력을 BGR에서 RGB로 변환
imgBGR = cv2.imread('/home/cherry/Desktop/Videos/file.avi')
imgRGB = cv2.cvtColor(imgBGR,cv2.COLOR_BGR2RGB)
 
# Matplotlib의 그래프 속성 지우기
plt.axis('off')
plt.imshow(imgRGB)
plt.show()
 
#그레이스케일영상출력
imgGray = cv2.imread('/home/cherry/Desktop/Videos/file.avi',cv2.IMREAD_GRAYSCALE)
 
# 그래프 속성 지우고 cmap으로 그레이 스케일 출력하기
plt.axis('off')
plt.imshow(imgGray,cmap='gray')
 
# 화면에 표시하는 기능
plt.show()