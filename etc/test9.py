import cv2

cap = cv2.VideoCapture('WalkingPutinRender.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Fast Video', frame)

    # 거의 지연 없이 재생
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
