import cv2
import mediapipe as mp

from customModule import getPoint, checkChoose, drawCalculator, listPoint, whatChooseCal, drawMain, whatChooseMain, \
    backToMain, drawBackToMain, drawPlayer, whatChoosePlayer, drawCamera, whatChooseCam

mp_drawling = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# real time web cam
capture = cv2.VideoCapture(0)

''' global variable '''
width, height = 870, 620

program = {'main': 1, 'cal': 0, 'cam': 0, 'music': 0}

positionPro = {
    'back': {
        'x': int(width * 3 / 4),
        'y': 10,
        'name': 'back'
    },
    'cal': {
        'x': int(width * 2 / 6),
        'y': int(height / 6),
        'name': 'cal'
    },
    'cam': {
        'x': int(width * 3 / 6) + 10,
        'y': int(height * 1 / 6),
        'name': 'cam'
    },
    'music': {
        'x': int(width * 4 / 6) + 10,
        'y': int(height * 1 / 6),
        'name': 'music'
    }
}

positionMusic = {
    'play': {
        'x': int(width * 2 / 4),
        'y': int(height * 2 / 4),
        'name': 'play',
    },
    'stop': {
        'x': int(width * 2 / 4),
        'y': int(height * 2 / 4),
        'name': 'stop',
    },
    'song': {
        'x': 20,
        'y': 50,
    }
}

positionCam = {
    'screenShot': {
        'x': int(width * 3 / 4),
        'y': int(height * 1 / 4),
        'name': 'screenShot',
    },
    'selfie': {
        'x': int(width * 3 / 4),
        'y': int(height * 2 / 4),
        'name': 'selfie',
    }
}
clickSong, isPlaying = False, False

# choose
choose = False
click = False
x_start = int(width / 2)
y_start = int(height / 7)
edgeBox = 80
listPt = listPoint(x_start, y_start, edgeBox)
bbThumb = 20
input1, input2, operator, result = '', '', '', ''

# run pro
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    pTime = 0
    while True:
        isTrue, frame = capture.read()
        # flip, resize frame, recolor
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # make detection
        results = holistic.process(frame)

        if results.left_hand_landmarks:
            landMark = results.left_hand_landmarks.landmark
            handLandMark = mp_holistic.HandLandmark

            # index finger tip
            x_tip_index, y_tip_index = getPoint(landMark, 8, width, height)
            frame = cv2.circle(frame, (x_tip_index, y_tip_index), 7, (0, 255, 0), thickness=-1)

            choose = checkChoose(landMark, x_tip_index, y_tip_index, width, height, bbThumb)

            # program main
            if program['main']:
                program = whatChooseMain(x_tip_index, y_tip_index, program, positionPro, choose, edgeBox)
                if (x_tip_index > int(width / 5) and x_tip_index < int(width / 5) + edgeBox) and (
                        y_tip_index > int(height / 7) and y_tip_index < int(height / 7) + edgeBox) and choose:
                    print('bye bye')
                    break

            if program['cal']:
                click, input1, input2, operator, result = whatChooseCal(listPt, choose, click, x_tip_index, y_tip_index,
                                                                        input1, input2, operator, result, edgeBox)

            # play music
            if program['music']:
                clickSong, isPlaying = whatChoosePlayer(x_tip_index, y_tip_index, choose, positionMusic, isPlaying,
                                                        clickSong)
            # play camera
            if program['cam']:
                click = whatChooseCam(frame, x_tip_index, y_tip_index, choose, click, positionCam)

            # back to main
            if not program['main']:
                program = backToMain(x_tip_index, y_tip_index, choose, program, positionPro)

                # display main menu
        if program['main']:
            frame = drawMain(frame, positionPro, edgeBox, width, height)

        # draw box calculator
        if program['cal']:
            frame, result, pTime = drawCalculator(frame, listPt, input1, input2, operator, result, x_start, height,
                                                  pTime)

        # interface for play music
        if program['music']:
            frame = drawPlayer(frame, positionMusic, isPlaying)

        # interface for camera
        if program['cam']:
            frame = drawCamera(frame, positionCam)

        # for back to main program
        if not program['main']:
            frame = drawBackToMain(frame, positionPro)

        # recolor
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('raw webcam', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

capture.release()
cv2.destroyAllWindows()
