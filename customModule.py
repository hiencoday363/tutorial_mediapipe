import mediapipe as mp
import cv2, math, time
from screenShot import startThread, threadMusic, threadScreenShoot, threadSelfie

thread1 = threadMusic('music/Lalala.mp3')
thScreenShoot = threadScreenShoot()


def drawMain(frame, positionPro, edgeBox, width, height):
    '''
    params:
    frame => frame of video,
    positionPro => dict of position of program box
    edge box => width = height of edge box
    return :
    frame
    '''
    # turn off program main
    frame = cv2.rectangle(frame, (int(width / 5), int(height / 7)),
                          (int(width / 5) + edgeBox, int(height / 7) + edgeBox),
                          (255, 0, 255), 2)
    frame = cv2.putText(frame, f"OFF", (int(width / 5) + 10, int(height / 7) + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2)

    for key, val in positionPro.items():
        if key == 'back':
            continue
        frame = cv2.rectangle(frame, (val['x'], val['y']), (val['x'] + edgeBox, val['y'] + edgeBox), (255, 0, 255), 2)

        frame = cv2.putText(frame, f"{key}", (val['x'] + 10, val['y'] + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2)

    return frame


def drawBackToMain(frame, positionPro):
    '''
    param: frame,
    positionPro => dict of position of program box
    return : frame
    '''
    frame = cv2.rectangle(frame, (positionPro['back']['x'], positionPro['back']['y']),
                          (positionPro['back']['x'] + 100, positionPro['back']['y'] + 70), (255, 0, 255), 2)

    frame = cv2.putText(frame, f"Back", (positionPro['back']['x'] + 20, positionPro['back']['y'] + 45),
                        cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)

    return frame


def backToMain(x_fin, y_fin, choose, program, positionPro):
    '''
    param:
    x_fin, y_fin = coordinate of index finger tip
    choose => check if choose
    program => all of program {main:1, cal:0, cam:0, music:0},
    positionPro => dict of position of program box
    return: frame, program
    '''

    if choose:
        if (x_fin > positionPro['back']['x'] and x_fin < positionPro['back']['x'] + 100) and (
                y_fin > positionPro['back']['y'] and y_fin < positionPro['back']['y'] + 70):
            for k in program:
                program[k] = 0
            program['main'] = 1

    return program


def whatChooseMain(x_fin, y_fin, program, positionPro, choose, edgeBox):
    '''
    params:
    x_fin, y_fin = coordinate of index finger tip
    program => all of program {main:1, cal:0, cam:0, music:0},
    positionPro => dict of position of program box
    edge box => width = height of edge box,
    choose => check if choose
    return :
    program
    '''
    for key, val in positionPro.items():
        if not choose:
            break
        if (x_fin > val['x'] and x_fin < val['x'] + edgeBox) and (y_fin > val['y'] and y_fin < val['y'] + edgeBox):
            for k in program:
                program[k] = 0
            program[key] = 1
    return program


def drawPlayer(frame, positionMusic, isPlaying):
    '''
    param: frame,
    positionMusic => dict of position of program player
    isPlaying => check playing or not
    return : frame
    '''
    frame = cv2.rectangle(frame, (positionMusic['stop']['x'], positionMusic['stop']['y']),
                          (positionMusic['stop']['x'] + 100, positionMusic['stop']['y'] + 70), (255, 0, 255), 2)

    if isPlaying:
        frame = cv2.putText(frame, f"stop", (positionMusic['stop']['x'] + 20, positionMusic['stop']['y'] + 45),
                            cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)

        frame = cv2.putText(frame, f"lalala", (positionMusic['song']['x'], positionMusic['song']['y']),
                            cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)
    else:
        frame = cv2.putText(frame, f"play", (positionMusic['stop']['x'] + 20, positionMusic['stop']['y'] + 45),
                            cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)

    return frame


def whatChoosePlayer(x_fin, y_fin, choose, positionMusic, isPlaying, clickSong):
    if (x_fin > positionMusic['play']['x'] and x_fin < positionMusic['play']['x'] + 100) and (
            y_fin > positionMusic['play']['y'] and y_fin < positionMusic['play']['y'] + 70) and choose:
        if not clickSong:
            clickSong = True
            isPlaying = not isPlaying
            if isPlaying:
                if not thread1.is_alive():
                    print('enjoy it')
                    startThread(thread1)
                else:
                    print('dang phat roi ma')
            else:
                print('khong tat nhac duoc anh oi')

    else:
        if clickSong:
            clickSong = False

    return clickSong, isPlaying


def drawCamera(frame, positionCam):
    '''
    param: frame,
    positionCam => dict of position of program camera
    return : frame
    '''
    for key, value in positionCam.items():
        if key == 'screenShot':
            frame = cv2.rectangle(frame, (value['x'], value['y']),
                                  (value['x'] + 180, value['y'] + 70), (255, 0, 255), 2)
        else:
            frame = cv2.rectangle(frame, (value['x'], value['y']),
                                  (value['x'] + 100, value['y'] + 70), (255, 0, 255), 2)

        frame = cv2.putText(frame, f"{key}", (value['x'] + 20, value['y'] + 45),
                            cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)

    return frame


def whatChooseCam(frame, x_fin, y_fin, choose, click, positionCam):
    if (x_fin > positionCam['screenShot']['x'] and x_fin < positionCam['screenShot']['x'] + 180) and (
            y_fin > positionCam['screenShot']['y'] and y_fin < positionCam['screenShot']['y'] + 70) and choose:
        if not click:
            click = True
            if not thScreenShoot.is_alive():
                print('let do it')
                startThread(thScreenShoot)

    elif (x_fin > positionCam['selfie']['x'] and x_fin < positionCam['selfie']['x'] + 100) and (
            y_fin > positionCam['selfie']['y'] and y_fin < positionCam['selfie']['y'] + 70) and choose:
        if not click:
            click = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            thSelfie = threadSelfie(frame)
            startThread(thSelfie)

    else:
        if click:
            click = False

    return click


def getPoint(landMark, index, w, h):
    '''
    parameter: landMark is a list of hands landmark,
    w, h: width , height frame
    index: 0 => wrist, 8 => index_finger_tip , ...
    return coordinate (x,y) pixel ---and--- z is dept, type: float
    '''
    x = int(landMark[index].x * w)
    y = int(landMark[index].y * h)
    # z = landMark[index].z

    return x, y


def checkChoose(landMark, x, y, w, h, wbb=20):
    '''
    parameter:
    landMark is a list of hands landmark,
    x is x_index_tip
    y is y_index_tip

    coordinate_index_finger = (x_index_tip, y_index_tip)
    w, h: width , height frame
    wbb: width bouding box

    return choose == true or false
    '''

    # thumb finger tip
    x_tip_thumb, y_tip_thumb = getPoint(landMark, 4, w, h)
    x_ip_thumb, y_ip_thumb = getPoint(landMark, 3, w, h)

    dis_tip_ip_thumb = math.sqrt(((x_tip_thumb - x_ip_thumb) ** 2 + (y_tip_thumb - y_ip_thumb) ** 2))
    dis_thumb_index = math.sqrt(((x_tip_thumb - x) ** 2 + (y_tip_thumb - y) ** 2))

    if dis_thumb_index < dis_tip_ip_thumb:
        return True
    return False
    # if (x < x_tip_thumb + wbb and x > x_tip_thumb - wbb) and (y < y_tip_thumb + wbb and y > y_tip_thumb - wbb):
    #     return True
    # return False


def listPoint(x, y, w_h_box):
    '''
    param:
    x => x start
    y => y start

    w_h_box => width=height box
    return: matrix of coordinate point
    '''
    a1 = w_h_box + 10
    a2 = a1 * 2
    a3 = a1 * 3

    return [
        [(x, y, '1'), (x + a1, y, '2'), (x + a2, y, '3'), (x + a3, y, '+')],

        [(x, y + a1, '4'), (x + a1, y + a1, '5'), (x + a2, y + a1, '6'), (x + a3, y + a1, '-')],

        [(x, y + a2, '7'), (x + a1, y + a2, '8'), (x + a2, y + a2, '9'), (x + a3, y + a2, 'x')],

        [(x, y + a3, '0'), (x + a1, y + a3, 'D'), (x + a2, y + a3, 'C'), (x + a3, y + a3, '/')]
    ]


def drawOnePt(frame, x_pt_1, y_pt_1, w_h_box, text):
    '''
    param:
    frame => frame,
    x_start => x start,
    y_start => y start,
    w_h_box => width == height
    text => 1-9, = - x / ,...
    return :
    frame
    '''
    x_text = x_pt_1 + int(w_h_box / 3)
    y_text = y_pt_1 + int(w_h_box / 3 * 2)

    frame = cv2.rectangle(frame, (x_pt_1, y_pt_1), (x_pt_1 + w_h_box, y_pt_1 + w_h_box), (0, 255, 0), 1)
    frame = cv2.putText(frame, f'{text}', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame


def drawCalculator(frame, matrix_pt, input1, input2, operator, result, x_start, height, pTime, w_h_box=80):
    '''
    param:
    frame => frame,
    matrix_pt => matrix of coordinate point,
    w_h_box => width = height box
    input1, input2, operator, result, x_start, height => for putText result
    pTime => for calculator time

    return :
    frame => da duoc draw
    '''

    # draw box: full
    for index_row, row in enumerate(matrix_pt):
        for index_col, (x, y, oper) in enumerate(row):
            frame = drawOnePt(frame, x, y, w_h_box, oper)

    # draw output
    if input1:
        frame = cv2.putText(frame, f'{input1}', (x_start, height - 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
    if operator:
        frame = cv2.putText(frame, operator, (x_start, height - 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
    if input2:
        frame = cv2.putText(frame, input2, (x_start, height - 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
        frame, result = drawResult(frame, input1, input2, operator, x_start, height - 40)

    # calculate fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # putText : fps
    frame = cv2.putText(frame, f'FPS: {fps:.2f}', (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame, result, pTime


def drawResult(frame, in1, in2, operator, x_start, y_start):
    '''
    param:
    frame => frame ,
    in1 => input first,
    in2 => input second,
    operator => ,
    x_start, y_start => coordinate
    return:
    frame with box result
    '''
    try:
        input1 = int(in1)
        input2 = int(in2)
    except:
        input1 = 0
        input2 = 0

    rs = ''
    if operator == '+':
        rs = input1 + input2
    elif operator == '-':
        rs = input1 - input2
    elif operator == 'x':
        rs = input1 * input2
    else:
        if input2 == 0:
            frame = cv2.putText(frame, 'an error occurred', (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 2)
            return frame

        else:
            rs = round(input1 / input2, 2)

    frame = cv2.putText(frame, f'= {rs}', (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

    return frame, rs


def whatChooseCal(listPt, choose, click, x_fin, y_fin, input1, input2, operator, result, edgeBox):
    '''
    param:
    listPt => matrix of coordinate point,
    choose => check choose or not
    click => avoid choose multi
    x_fin, y_fin = coordinate of index finger tip
    input1, operator, input2, result => num1 operator num2 = result
    edgeBox => edge of box
    return click, input1, input2, operator, result
    '''

    if (x_fin > listPt[3][0][0] and x_fin < listPt[3][0][0] + edgeBox) and (
            y_fin > listPt[3][0][1] and y_fin < listPt[3][0][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '0'
            else:
                input1 += '0'

    elif (x_fin > listPt[0][0][0] and x_fin < listPt[0][0][0] + edgeBox) and (
            y_fin > listPt[0][0][1] and y_fin < listPt[0][0][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '1'
            else:
                input1 += '1'

    elif (x_fin > listPt[0][1][0] and x_fin < listPt[0][1][0] + edgeBox) and (
            y_fin > listPt[0][1][1] and y_fin < listPt[0][1][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '2'

            else:
                input1 += '2'

    elif (x_fin > listPt[0][2][0] and x_fin < listPt[0][2][0] + edgeBox) and (
            y_fin > listPt[0][2][1] and y_fin < listPt[0][2][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '3'

            else:
                input1 += '3'

    elif (x_fin > listPt[1][0][0] and x_fin < listPt[1][0][0] + edgeBox) and (
            y_fin > listPt[1][0][1] and y_fin < listPt[1][0][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '4'
            else:
                input1 += '4'

    elif (x_fin > listPt[1][1][0] and x_fin < listPt[1][1][0] + edgeBox) and (
            y_fin > listPt[1][1][1] and y_fin < listPt[1][1][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '5'

            else:
                input1 += '5'

    elif (x_fin > listPt[1][2][0] and x_fin < listPt[1][2][0] + edgeBox) and (
            y_fin > listPt[1][2][1] and y_fin < listPt[1][2][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '6'

            else:
                input1 += '6'

    elif (x_fin > listPt[2][0][0] and x_fin < listPt[2][0][0] + edgeBox) and (
            y_fin > listPt[2][0][1] and y_fin < listPt[2][0][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '7'
            else:
                input1 += '7'

    elif (x_fin > listPt[2][1][0] and x_fin < listPt[2][1][0] + edgeBox) and (
            y_fin > listPt[2][1][1] and y_fin < listPt[2][1][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '8'

            else:
                input1 += '8'

    elif (x_fin > listPt[2][2][0] and x_fin < listPt[2][2][0] + edgeBox) and (
            y_fin > listPt[2][2][1] and y_fin < listPt[2][2][1] + edgeBox) and choose:
        if not click:
            click = True
            if operator:
                input2 += '9'

            else:
                input1 += '9'

    elif (x_fin > listPt[0][3][0] and x_fin < listPt[0][3][0] + edgeBox) and (
            y_fin > listPt[0][3][1] and y_fin < listPt[0][3][1] + edgeBox) and choose:
        if not click:
            click = True
            if result:
                input1 = result
                input2 = ''
                operator = '+'
            else:
                operator = '' if not input1 else '+'

    elif (x_fin > listPt[1][3][0] and x_fin < listPt[1][3][0] + edgeBox) and (
            y_fin > listPt[1][3][1] and y_fin < listPt[1][3][1] + edgeBox) and choose:
        if not click:
            click = True
            if result:
                input1 = result
                input2 = ''
                operator = '-'
            else:
                operator = '' if not input1 else '-'

    elif (x_fin > listPt[2][3][0] and x_fin < listPt[2][3][0] + edgeBox) and (
            y_fin > listPt[2][3][1] and y_fin < listPt[2][3][1] + edgeBox) and choose:
        if not click:
            click = True
            if result:
                input1 = result
                input2 = ''
                operator = 'x'
            else:
                operator = '' if not input1 else 'x'

    elif (x_fin > listPt[3][3][0] and x_fin < listPt[3][3][0] + edgeBox) and (
            y_fin > listPt[3][3][1] and y_fin < listPt[3][3][1] + edgeBox) and choose:
        if not click:
            click = True
            if result:
                input1 = result
                input2 = ''
                operator = '/'
            else:
                operator = '' if not input1 else '/'

    elif (x_fin > listPt[3][2][0] and x_fin < listPt[3][2][0] + edgeBox) and (
            y_fin > listPt[3][2][1] and y_fin < listPt[3][2][1] + edgeBox) and choose:
        if not click:
            click = True
            input1, input2, operator, result = '', '', '', ''

    elif (x_fin > listPt[3][1][0] and x_fin < listPt[3][1][0] + edgeBox) and (
            y_fin > listPt[3][1][1] and y_fin < listPt[3][1][1] + edgeBox) and choose:
        if not click:
            click = True
            if not operator and input1:
                input1 = input1[:-1]
            else:
                if input2:
                    input2 = input2[:-1]

    else:
        if click:
            click = False
            print('out')

    return click, input1, input2, operator, result
