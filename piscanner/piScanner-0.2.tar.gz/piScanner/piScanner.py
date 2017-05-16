import cv2
import numpy as np
import rect
import mouse
import linedr


class deepScan(object):
    ''' To Scan an Image, say img.jpg
        -----------------------------

        1. scanner = deepScan("img.jpg")
        2. Without this step, you can't move further. scanner.scan()

        Now you can use all the functions of the script.
        To see functions type "help(scanner)".

        Note: 1. self.show_scanned() will show you the final scanned image. This
                is the image we finally need.

              2. To save any image, once it is opened, click 's'. It will close the
                  window and save the image automatically in working directory.
        
        '''
    def __init__(self, image_adr):
        self.image = cv2.imread(image_adr)
        self.scanned = ''
        self.gauss = ''
        self.mean = ''

    def scan(self, resize = False, width = 1500, height = 880):
        ''' Main function, which scans the image. '''
        
        # add image here.
        # We can also use laptop's webcam if the resolution is good enough to capture
        # readable document content
        image = self.image

        # resize image so it can be processed
        # choose optimal dimensions such that important content is not lost
        if resize: 
            image = cv2.resize(image, (width, height))
    
        crd = mouse.run(image)
        
        crop = image[int(crd[1]):int(crd[3]), int(crd[0]):int(crd[2])]
        
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        
        
        retr,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

        self.scanned = thresh
        self.mean = th2
        self.gauss = th3
        
        
        self.show_scanned()
        

    def cng_perspective(self, image, map_to):

        croods = linedr.LineDrawer(image)
        cords = croods.draw_line()

        cord1 = list(cords[0])
        cord2 = list(cords[1])
        cord3 = list(cords[2])
        cord4 = list(cords[3])
        
        pts1 = np.float32([cord1, cord2, cord3, cord4])
        pts2 = np.float32([[0,0],[map_to,0],[map_to,map_to],[0,map_to]])

        M = cv2.getPerspectiveTransform(pts1,pts2)
        dst = cv2.warpPerspective(image,M,(map_to,map_to))

        return dst

    def rotate(self, image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
     
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
     
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
     
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
     
        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))
        
        
    def show_scanned(self):
        self.__show("Scanned Image", self.scanned)

    def show_gaussian_threshold(self):
        self.__show("Gaussian Threshold Image", self.gauss)

    def show_mean_threshold(self):
        self.__show("Mean Threshold Image", self.mean)

    def show_orignal_image(self):
        self.__show("Original Image", self.image)

    def __show(self, title, image):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, image)
        
        if(cv2.waitKey(0) == ord('s')):
            self.__save_as(title, '.png', image)
        cv2.destroyAllWindows()
    
    def __save_as(self, name, extension, image):
        cv2.imwrite(name+extension, image)
