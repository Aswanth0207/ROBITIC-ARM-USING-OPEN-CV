import cv2
import mediapipe as mp
import time
import serial

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=False):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])

                if draw and id == 0:
                    cv2.circle(frame, (cx, cy), 15, (255, 0, 255), -1)
        return lmList

def main():
    prevTime = 0
    currentTime = 0
    hand = [["Wrist", False], ["Index", False], ["Middle", False], 
            ["Ring", False], ["Thumb", False], ["Pinky", False]]


    ser = serial.Serial(port="COM5")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = HandDetector()

    while (True):
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)

        if len(lmList) > 0: 

            j = 1
            change = False
            for i in range(1, 6):
                if i == 1 and lmList[4][1] < lmList[3][1] and not hand[4][1]:
                    hand[4][1] = True
                    change = True
                    print(hand[4][0], hand[4][1])
                elif i == 1 and lmList[4][1] > lmList[3][1] and hand[4][1]:
                    hand[4][1] = False
                    change = True
                    print(hand[4][0], hand[4][1])
                elif i != 1:
                    if lmList[i*4][2] > lmList[(i*4)-2][2] and not hand[j][1]:
                        hand[j][1] = True
                        change = True
                        print(hand[j][0], hand[j][0])
                    elif lmList[i*4][2] < lmList[(i*4)-2][2] and hand[j][1]:
                        hand[j][1] = False
                        change = True
                        print(hand[j][0], hand[j][0])
                    if j == 3:
                        j += 2
                    else:
                        j += 1

            if change:
                msg = ""
                for i in range(6):
                    if hand[i][1]:
                        msg += "1"
                    else:
                        msg += "0"

                msg += '\n'
                print(msg)
                ser.write(msg.encode("Ascii")) 

        currentTime = time.time()
        fps = 1/(currentTime-prevTime)
        prevTime = currentTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

main()