import cv2
from os import sep
from config import *
from math import sin, cos

pixel = lambda img, x, y: img[y, x][::-1]
debug = False


def circle_coors(p1, p2):
    x, y, r, l = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2, abs((p1[0]-p2[0])/2), []
    for i in range(360):
        c = (int(cos(i)*r+x), int(sin(i)*r+y))
        if not c in l:
            l.append(c)
    return l


def detect(img, coors):
    whites = 0
    for (x, y) in coors:
        #print(x, y)
        r, g, b = pixel(img, x, y)
        img[y, x] = [255,0,0]
        #print(r, g, b)
        whites += int(r >= WT and g >= WT and b >= WT)
    return (whites/len(coors)) >= PT


def main(coors, fl=FILE):
    vidcap, success = cv2.VideoCapture("videos"+sep+fl), True
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE) if debug else 0

    i, last = 0, 0
    frames = []
    while True:
        #print(i)
        success, image = vidcap.read()
        if not success:
            break
        if detect(image, coors):
            if (i - last) > 60*ADHD:
                frames.append(i/vidcap.get(cv2.CAP_PROP_FPS))
            last = i
        cv2.imshow("video", image) if debug else 0
        
        i += 1
        cv2.waitKey(0) if debug else 0
    
    vidcap.release()
    cv2.destroyAllWindows() if debug else 0
    return frames


if __name__ == "__main__":
    print(main(circle_coors(P1, P2)))
    #print(detect(cv2.imread("/data/python/out.png")))
