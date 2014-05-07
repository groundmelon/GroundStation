import numpy as np
import cv2
import time

if __name__ =='__main__':
    cap = cv2.VideoCapture('test.avi')
    cap = cv2.VideoCapture(0)
    
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 20,
                           qualityLevel = 0.3,
                           minDistance = 20,
                           blockSize = 7 )
    
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 4,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
                      # criteria = (cv2.TERM_CRITERIA_EPS, 10, 0.03))
    
    # Create some random colors
    color = np.random.randint(0,255,(100,3))
    
    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    ###############
    # old_frame = cv2.resize(old_frame, (640,360), interpolation = cv2.INTER_CUBIC)
    ##############
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    
    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    
    while(1):
        ret,frame = cap.read()
        if frame == None:
            break
        #################
    #     frame = cv2.resize(frame, (640,360), interpolation = cv2.INTER_CUBIC)
        ###############
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        a = time.clock()
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        print '%4.4f'%((time.clock()-a)*1000)
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
        
        v = [ ((n[0]-o[0])**2+(n[1]-o[1])**2)**0.5 for n,o in zip(good_new, good_old)]
    #     print ['%4.4f'%x for x in v]
        
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(frame,mask)
    
        cv2.imshow('frame',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)
    
    cv2.destroyAllWindows()
    cap.release()
