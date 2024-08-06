import cv2
import socket
import time
import cv2 as cv
import numpy as np
import requests
import imutils

url = "http://192.168.43.172:8080/shot.jpg"
'''
def LOT(a,b,c,d):
    a1 = b[1] - a[1]
    b1 = a[1] - b[0]
    c1 = a1*a[0] + b1*a[1]

    a2 = d[1] - c[1]
    b2 = c[0] - d[0]
    c2 = a2*c[0] + b2*c[1]

    det = a1 *b2 - a2*b1

    if det == 0:
        return [10000,10000]
    else:
        x = (b2*c1 - b1*c2)/det
        y = (a1*c2 - a2*c1)/det
        return [x,y]
'''

def centroid(a,b,c,d):
    len_mid_y = (a[1] + b[1])/2
    if abs(a[0]) < abs(b[0]):
        len_mid_x = a[0]
    else:
        len_mid_x = b[0]

    wid_mid_y = (c[0]+d[0])/2
    wid_mid_x = (c[1]+d[1])/2


    cen_mid_x = (len_mid_x + wid_mid_x)/2
    cen_mid_y = (len_mid_y + wid_mid_y)/2

    return [cen_mid_x,cen_mid_y]
'''
def centroid(max_contour):
    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        return [cx,cy]
    else:
        return None
'''

itr = 1
while(True):

    #cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #ret, frame = cap.read()

    #if ret == False:
        #print('Cannot find camera!')
        #break
    #elif frame.shape[0] != 480 or frame.shape[1] != 640:
        #print('Wrong frame width or height! (need 640 for width and 480 for height)')
        #break



    ################################### Socket #######################################
    HOST = '127.0.0.1'
    PORT = 9000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # tcp
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse tcp
    sock.bind((HOST, PORT))
    sock.listen(1)

    print('Wait for connection...')
    (client, adr) = sock.accept()
    print("Client Info: ", client, adr)

    frame_rate = 0.8
    prev = 0
    fps_time = 1.0
    while(True):
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=640, height=480)
        img2 = imutils.resize(img, width=640, height=480)
        cv2.imshow("Android_cam", img)
        frame = img
        frame2 = img2

        #ret, frame = cap.read()
        #rt,frame2  = cap.read()

        ###############################Points detection###########################

        #cv.imshow('palm image',frame)

        hsvim = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower = np.array([0, 48, 80], dtype = "uint8")
        upper = np.array([20, 255, 255], dtype = "uint8")
        skinRegionHSV = cv.inRange(hsvim, lower, upper)
        blurred = cv.blur(skinRegionHSV, (2,2))
        rt,thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)

        #cv.imshow("thresh", thresh)

        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = max(contours, key=lambda x: cv.contourArea(x))

        #cent = centroid(contours)

        #print(str(contours))
        cv.drawContours(frame, [contours], -1, (255,255,0), 2)
        #cv.imshow("contours", frame)


        hull = cv.convexHull(contours)
        cv.drawContours(frame, [hull], -1, (0, 255, 255), 2)
        #cv.imshow("hull", frame)

        #print(hull)

        #print("********************************************************")

        x_axis = []
        y_axis = []

        for i in hull:
            x_axis.append(i[0][0])
            y_axis.append(i[0][1])

        x_max, x_min = max(x_axis), min(x_axis)
        y_max, y_min = max(y_axis), min(y_axis)


        sent_arr = []
        sent_arr.append(x_max)
        sent_arr.append(x_min)
        sent_arr.append(y_max)
        sent_arr.append(y_min)
        #print(sent_arr)
        centroid_val = []
        y_m_flag = 0
        x_m_flag = 0
        y_flag = 0
        x_flag = 0
        for h in hull:
            x = h[0][0]
            y = h[0][1]
            if y_m_flag == 0 and y == y_max:
                centroid_val.append([x,y])
                y_m_flag = 1
            if y_flag == 0 and  y == y_min:
                centroid_val.append([x,y])
                y_flag = 1
            if x_m_flag == 0 and x == x_max:
                centroid_val.append([x,y])
                x_m_flag = 1
            if x_flag == 0 and x == x_min:
                centroid_val.append([x,y])
                x_flag = 1

        cent = centroid(centroid_val[0], centroid_val[1], centroid_val[2], centroid_val[3])

        '''
        
        for h in hull:
            x = h[0][0]
            y = h[0][1]
            if y == y_max:
                cv2.circle(frame, (x, y), 3, (0, 0, 0), -1)
            if y == y_min:
                cv2.circle(frame, (x, y), 3, (128, 128, 0), -1)
            if x == x_max:
                cv2.circle(frame, (x, y), 3, (0, 0, 0), -1)
            if x == x_min:
                cv2.circle(frame, (x, y), 3, (128, 128, 0), -1)
        hull = cv.convexHull(contours, returnPoints=False)
        defects = cv.convexityDefects(contours, hull)
        '''

        '''
        if defects is not None:
            cnt = 0
        for i in range(defects.shape[0]):  # calculate the angle
            s, e, f, d = defects[i][0]
            start = tuple(contours[s][0])
            end = tuple(contours[e][0])
            far = tuple(contours[f][0])
            a = np.sqrt((end[0] - start[0]) * 2 + (end[1] - start[1]) * 2)
            b = np.sqrt((far[0] - start[0]) * 2 + (far[1] - start[1]) * 2)
            c = np.sqrt((end[0] - far[0]) * 2 + (end[1] - far[1]) * 2)
            angle = np.arccos((b * 2 + c * 2 - a ** 2) / (2 * b * c))  # cosine theorem
            if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
                cnt += 1
                # cv.circle(img, far, 4, [0, 0, 255], -1)
        if cnt > 0:
            cnt = cnt+1
        cv.putText(frame, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv.LINE_AA)
        '''

        #cv.imshow('final_result',frame)

        ##cv2.waitKey(0)

        #############################Point detect End###############################

        result, encimg = cv2.imencode('.jpeg', frame2, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

        temp = client.recv(1024)


        client.send(str(len(encimg.flatten())).encode('utf-8'))
        print('number of frame :',itr)
        itr+=1

        temp = client.recv(1024)

        client.send(encimg)

        temp = client.recv(1024)

        keypoint_str = str(int(sent_arr[0])) + ',' + str(int(sent_arr[1])) + ',' + str(int(sent_arr[2])) + ',' + str(int(sent_arr[3]))
        client.send(bytes(keypoint_str, 'ascii'))

        cent_str = keypoint_str = str(cent[0]) + ',' + str(cent[1])
        client.send(bytes(cent_str, 'ascii'))

        cv2.putText(frame2, "FPS: %f" % (1.0/(time.time() - fps_time)), (30, 30),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('frame', frame2)
        cv2.waitKey(1)
        fps_time = time.time()
        time.sleep(0.3)