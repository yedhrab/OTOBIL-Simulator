import cv2
import numpy as np
import math
import numpy as np


def should_car_turn(img):
    """
    furkan 2 serit arasında durması gerektiğinde true vericek
    durması gerekmezse false vericek
    (!piksel degerlerinde sıkıntı var,bu sorun çözülmeli)
    """
    
    #RESMİ BELLEĞE ALMAK
    
    #2.yol
    #cv2 
    # Load an color image in grayscale
              
    #------------------------------------------------------------------------------
    #KENAR ALGILAMA
    # Burada gri tonlamaya dönüştür. 
    gray_image = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    # Canny Edge Detection'ı buradan arayın. 
    cannyed_image = cv2.Canny (gray_image, 60, 120)
    
    #------------------------------------------------------------------------------
    #RESMİN İLGİLİ BÖLGESİNİ ALMAK
    
    height, width, channels = img.shape
    region_of_interest_vertices = [(0, height-int(height*0.041)),
                              (0, height-int(height*0.2)),
                              (int(width/2)-int(width*0.078),height-int(height*0.416)),
                              (int(width/2) + int(width*0.078),height-int(height*0.416)),
                              (width,height-int(height*0.2)),
                              (width,height-int(height*0.041)),]
    #daha sonra bulunan noktaları matris olarak vermeliyim
    #------------------------------------------------------------------------------
    #RESMİN İLGİLİ BÖLGESİNİ KIRPMAK
    def region_of_interest(img, vertices):
        # Define a blank matrix that matches the image height/width.
        mask = np.zeros_like(img)
        # Retrieve the number of color channels of the image.
        channel_count = 4
        # Create a match color with the same color channel counts.
        match_mask_color = (255,) * channel_count
          
        # Fill inside the polygon
        cv2.fillPoly(mask, vertices, match_mask_color)
        
        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)
        
        cv2.imshow("deneme", masked_image)
        cv2.waitKey(30)

        return masked_image
    
    
    cropped_image = region_of_interest(cannyed_image,np.array([region_of_interest_vertices], np.int32),)

    #------------------------------------------------------------------------------
    #KENAR piksellerinden serit oluşturmak
    lines = cv2.HoughLinesP(cropped_image,rho=6,theta=np.pi / 60,threshold=160,lines=np.array([]),
        minLineLength=40,maxLineGap=25)
    #------------------------------------------------------------------------------
    #LİNES DEGERLERİ İLE ORJİNAL RESİMDE SERİT ÇİZİMİ
    def draw_lines(img, lines, color=[0, 0, 255], thickness=3):
        # If there are no lines to draw, exit.
        if lines is None:
            return
        # Make a copy of the original image.
        img = np.copy(img)
        # Create a blank image that matches the original in size.
        line_img = np.zeros((img.shape[0],img.shape[1],channels),dtype=np.uint8,)
        # Loop over all lines and draw them on the blank image.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
                # Merge the image with the lines onto the original.
        
                img = cv2.addWeighted(img,0.8,line_img,1.0, 0.0)
                # Return the modified image.
        return img


    #---------------------------------------------------------------------------------------
    min_line_y = 0
    max_line_y = height
    piksel1=0
    piksel2=1000
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
            if math.fabs(slope) > 0.1: # <-- Only consider extreme slope,eğim yatay değilse cık
                continue
            if int((y1+y2)/2) > min_line_y :  # <-- Otherwise, right group.
                min_line_y=int((y1+y2)/2)
                
            if int((y1+y2)/2) < max_line_y :
                max_line_y=int((y1+y2)/2)
                    
    piksel1=height-min_line_y
    #cv2.putText(img,"yakin serit"+str(piksel1),(100,100), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 255), 3)
    #img = draw_lines(img,[[[int(width/2),int(height),int(width/2),min_line_y],]],[0,255,255],5)
    if  max_line_y+int(height*0.03)< min_line_y:
        piksel2=height-max_line_y 
        #cv2.putText(img,"uzak serit"+str(piksel2),(100,200), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
        #img = draw_lines(img,[[[int(width/2)+20,int(height),int(width/2)+20,max_line_y ],]],[0,0,255],5)
    if piksel1<int(height*0.25):#150-132
        if piksel2<int(height*0.45):#270-240
            #cv2.putText(img,"True",(100,300), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
            return True
        else:
            #cv2.putText(img,"False",(100,400), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
            return False
    else:
        #cv2.putText(img,"False",(100,500), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
        return False


def is_stop_point(img):
    """
    furkan 2 serit arasında durması gerektiğinde true vericek
    durması gerekmezse false vericek
    (!piksel degerlerinde sıkıntı var,bu sorun çözülmeli)
    """
    
    #RESMİ BELLEĞE ALMAK
    
    #2.yol
    #cv2 
    # Load an color image in grayscale
              
    #------------------------------------------------------------------------------
    #KENAR ALGILAMA
    # Burada gri tonlamaya dönüştür. 
    gray_image = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    # Canny Edge Detection'ı buradan arayın. 
    cannyed_image = cv2.Canny (gray_image, 60, 120)
    
    #------------------------------------------------------------------------------
    #RESMİN İLGİLİ BÖLGESİNİ ALMAK
    
    height, width, channels = img.shape
    region_of_interest_vertices = [(0, height-int(height*0.041)),
                              (0, height-int(height*0.2)),
                              (int(width/2)-int(width*0.078),height-int(height*0.416)),
                              (int(width/2) + int(width*0.078),height-int(height*0.416)),
                              (width,height-int(height*0.2)),
                              (width,height-int(height*0.041)),]
    #daha sonra bulunan noktaları matris olarak vermeliyim
    #------------------------------------------------------------------------------
    #RESMİN İLGİLİ BÖLGESİNİ KIRPMAK
    def region_of_interest(img, vertices):
        # Define a blank matrix that matches the image height/width.
        mask = np.zeros_like(img)
        # Retrieve the number of color channels of the image.
        channel_count = 4
        # Create a match color with the same color channel counts.
        match_mask_color = (255,) * channel_count
          
        # Fill inside the polygon
        cv2.fillPoly(mask, vertices, match_mask_color)
        
        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)
        
        return masked_image
    
    
    cropped_image = region_of_interest(cannyed_image,np.array([region_of_interest_vertices], np.int32),)

    #------------------------------------------------------------------------------
    #KENAR piksellerinden serit oluşturmak
    lines = cv2.HoughLinesP(cropped_image,rho=6,theta=np.pi / 60,threshold=160,lines=np.array([]),
        minLineLength=40,maxLineGap=25)
    #------------------------------------------------------------------------------
    #LİNES DEGERLERİ İLE ORJİNAL RESİMDE SERİT ÇİZİMİ
    def draw_lines(img, lines, color=[0, 0, 255], thickness=3):
        # If there are no lines to draw, exit.
        if lines is None:
            return
        # Make a copy of the original image.
        img = np.copy(img)
        # Create a blank image that matches the original in size.
        line_img = np.zeros((img.shape[0],img.shape[1],channels),dtype=np.uint8,)
        # Loop over all lines and draw them on the blank image.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
                # Merge the image with the lines onto the original.
        
                img = cv2.addWeighted(img,0.8,line_img,1.0, 0.0)
                # Return the modified image.
        return img


    #---------------------------------------------------------------------------------------
    min_line_y = 0
    max_line_y = height
    piksel1=0
    piksel2=1000
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
            if math.fabs(slope) > 0.1: # <-- Only consider extreme slope,eğim yatay değilse cık
                continue
            if int((y1+y2)/2) > min_line_y :  # <-- Otherwise, right group.
                min_line_y=int((y1+y2)/2)
                
            if int((y1+y2)/2) < max_line_y :
                max_line_y=int((y1+y2)/2)
                    
    piksel1=height-min_line_y
    #cv2.putText(img,"yakin serit"+str(piksel1),(100,100), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 255), 3)
    #img = draw_lines(img,[[[int(width/2),int(height),int(width/2),min_line_y],]],[0,255,255],5)
    if  max_line_y+int(height*0.03)< min_line_y:
        piksel2=height-max_line_y 
        #cv2.putText(img,"uzak serit"+str(piksel2),(100,200), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
        #img = draw_lines(img,[[[int(width/2)+20,int(height),int(width/2)+20,max_line_y ],]],[0,0,255],5)
    if piksel1<int(height*0.25):#150-132
        if piksel2<int(height*0.45):#270-240
            #cv2.putText(img,"True",(100,300), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
            return True
        else:
            #cv2.putText(img,"False",(100,400), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
            return False
    else:
        #cv2.putText(img,"False",(100,500), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 0, 255), 3)
        return False


def is_finishing_line(img):
    """
    Determine if the line is finishing line

    If finishing line ---> @return {True}

    Else ---> @return {False}

    """

    # RESMİ BELLEĞE ALMAK

    # 2.yol
    # cv2
    # Load an color image in grayscale

    # ------------------------------------------------------------------------------
    # KENAR ALGILAMA
    # Burada gri tonlamaya dönüştür.
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Canny Edge Detection'ı buradan arayın.
    cannyed_image = cv2.Canny(gray_image, 110, 200)

    # ------------------------------------------------------------------------------
    # RESMİN İLGİLİ BÖLGESİNİ ALMAK

    height, width, channels = img.shape
    region_of_interest_vertices = [(0, height-int(height*0.041)),
                                   (0, height-int(height*0.2)),
                                   (int(width/2)-int(width*0.078),
                                    height-int(height*0.416)),
                                   (int(width/2) + int(width*0.078),
                                    height-int(height*0.416)),
                                   (width, height-int(height*0.2)),
                                   (width, height-int(height*0.041)), ]
    # daha sonra bulunan noktaları matris olarak vermeliyim
    # ------------------------------------------------------------------------------
    # RESMİN İLGİLİ BÖLGESİNİ KIRPMAK

    def region_of_interest(img, vertices):
        # Define a blank matrix that matches the image height/width.
        mask = np.zeros_like(img)
        # Retrieve the number of color channels of the image.
        channel_count = 4
        # Create a match color with the same color channel counts.
        match_mask_color = (255,) * channel_count

        # Fill inside the polygon
        cv2.fillPoly(mask, vertices, match_mask_color)

        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)

        return masked_image

    cropped_image = region_of_interest(cannyed_image, np.array(
        [region_of_interest_vertices], np.int32),)

    # ------------------------------------------------------------------------------
    # KENAR piksellerinden serit oluşturmak
    lines = cv2.HoughLinesP(cropped_image, rho=6, theta=np.pi / 60, threshold=160, lines=np.array([]),
                            minLineLength=40, maxLineGap=25)

    # ------------------------------------------------------------------------------

    def draw_lines(img, lines, color=[0, 0, 255], thickness=3):
        # If there are no lines to draw, exit.
        if lines is None:
            return
        # Make a copy of the original image.
        img = np.copy(img)
        # Create a blank image that matches the original in size.
        line_img = np.zeros(
            (img.shape[0], img.shape[1], channels), dtype=np.uint8,)
        # Loop over all lines and draw them on the blank image.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
                # Merge the image with the lines onto the original.
        img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
        # Return the modified image.
        return img
    # ---------------------------------------------------------------------------------------
    # SERİTLERİN EĞİMİNİ BULMAK

    min_line_y = 0
    piksel = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)  # <-- Calculating the slope.
            if math.fabs(slope) > 0.1:  # <-- Only consider extreme slope,eğim yatay değilse cık
                continue
            elif int((y1+y2)/2) > min_line_y:  # <-- Otherwise, right group.
                min_line_y = int((y1+y2)/2)

    piksel = height-min_line_y
    if(piksel < int(height*0.41)):
        return True
    else:
        return False


def detect_turn_direction(img):
    """
    Determine the turn direction 

    @return -1 if direction is left

    @return 1 if direction is right

    Other cases return 0{No effect}

    """
    # RESMİ BELLEĞE ALMAK

    # 2.yol
    # cv2
    # Load an color image in grayscale

    # ------------------------------------------------------------------------------
    # KENAR ALGILAMA
    # Burada gri tonlamaya dönüştür.
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Canny Edge Detection'ı buradan arayın.
    cannyed_image = cv2.Canny(gray_image, 60, 120)

    # ------------------------------------------------------------------------------
    # RESMİN İLGİLİ BÖLGESİNİ ALMAK

    height, width, channels = img.shape
    region_of_interest_vertices = [(0, height-int(height*0.041)),
                                   (0, height-int(height*0.2)),
                                   (int(width/2)-int(width*0.078),
                                    height-int(height*0.416)),
                                   (int(width/2) + int(width*0.078),
                                    height-int(height*0.416)),
                                   (width, height-int(height*0.2)),
                                   (width, height-int(height*0.041)), ]
    # daha sonra bulunan noktaları matris olarak vermeliyim
    # ------------------------------------------------------------------------------
    # RESMİN İLGİLİ BÖLGESİNİ KIRPMAK

    def region_of_interest(img, vertices):
        # Define a blank matrix that matches the image height/width.
        mask = np.zeros_like(img)
        # Retrieve the number of color channels of the image.
        channel_count = 4
        # Create a match color with the same color channel counts.
        match_mask_color = (255,) * channel_count

        # Fill inside the polygon
        cv2.fillPoly(mask, vertices, match_mask_color)

        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)

        return masked_image

    cropped_image = region_of_interest(cannyed_image, np.array(
        [region_of_interest_vertices], np.int32),)

    # ------------------------------------------------------------------------------
    # KENAR piksellerinden serit oluşturmak
    lines = cv2.HoughLinesP(cropped_image, rho=6, theta=np.pi / 60, threshold=160, lines=np.array([]),
                            minLineLength=40, maxLineGap=25)

    # ------------------------------------------------------------------------------
    # SERİTLERİN EĞİMİNİ BULMAK

    left_line_y = []
    right_line_y = []

    left_line_y_max = height
    right_line_y_max = height

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)  # <-- Calculating the slope.
            if math.fabs(slope) < 0.5:  # <-- Only consider extreme slope
                continue
            if slope <= 0:  # <-- If the slope is negative, left group.
                left_line_y.extend([y1, y2])
            else:  # <-- Otherwise, right group.
                right_line_y.extend([y1, y2])

    for y in left_line_y:
        if y < left_line_y_max:
            left_line_y_max = y

    for y in right_line_y:
        if y < right_line_y_max:
            right_line_y_max = y

    if right_line_y_max > 50+left_line_y_max:
        return -1
    elif right_line_y_max+50 < left_line_y_max:
        return +1
    else:
        return 0


def find_turn_angle(image):
    """Dönüş açısını hesaplama
    0 -> Sol
    1 -> Sağ

    Arguments:
        image {np.array} -- Resim

    Returns:
        Hata varsa -1
        np.array, tuple -- Resim ve dönüş bilgileri (0, 58.5)

    Examples:
        image, donus_data = find_turn_angle(image)
        yon, donus_pixel_uzunlugu = donus_data
    """

    is_kawis = 0
    avg_slope = []

    def canny_img(image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.GaussianBlur(image, (15, 15), 0)
        return cv2.Canny(image, 50, 150)

    def region_of_interest(image):
        height, width = image.shape
        points = [
            (width * 0, height * 1),
            (width * 0.1, height * 0.8),
            (width * 0.25, height * 0.6),
            (width * 0.75, height * 0.6),
            (width * 0.90, height * 0.8),
            (width * 1, height * 1),
        ]
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, np.array([points], np.int32), 255)
        return cv2.bitwise_and(image, mask)

    def hough_lines(image):
        return cv2.HoughLinesP(
            image,
            rho=1,
            theta=np.pi / 180,
            threshold=40,
            minLineLength=50,
            maxLineGap=100
        )

    def avarage_slope(lines):
        left_avg = (0., 0.)
        right_avg = (0., 0.)

        if lines is not None:

            left_lines = []
            right_lines = []

            for line in lines:
                for x0, y0, x1, y1 in line:
                    if x0 == x1:
                        continue

                    slope = (y1 - y0) / (x1 - x0)
                    intercept = y0 - (slope * x0)

                    if slope < 0:
                        left_lines.append((slope, intercept))
                    else:
                        right_lines.append((slope, intercept))

                    if len(left_lines) > 0:
                        left_avg = np.average(left_lines, axis=0)
                    if len(right_lines) > 0:
                        right_avg = np.average(right_lines, axis=0)

            return left_avg, right_avg

    def slope_to_point(y0, y1, line_slope):
        if line_slope[0] != 0:  # infinite kontrolu
            x0 = int((y0 - line_slope[1]) / line_slope[0])
            x1 = int((y1 - line_slope[1]) / line_slope[0])
        else:
            x0 = 0
            x1 = 0
        return x0, y0, x1, y1

    def avarage_lanes(image, lines):
        nonlocal avg_slope

        avg_lane = avarage_slope(lines)
        avg_slope = avg_lane

        y0 = image.shape[0]
        y1 = int(y0 * 0.6)

        # Sol serit yoksa 0 dondur.
        if avg_lane[0][0] == 0 and avg_lane[0][1] == 0:
            left_line = (0, 0, 0, 0)
        else:
            left_line = slope_to_point(y0, y1, avg_lane[0])

        # Sag serit yoksa 0 dondur.
        if avg_lane[1][0] == 0 and avg_lane[1][1] == 0:
            right_line = (0, 0, 0, 0)
        else:
            right_line = slope_to_point(y0, y1, avg_lane[1])

        return left_line, right_line

    # TODO Kalınlığı düzelt
    def draw_lines(image, lines, color=[255, 0, 0], thickness=40):
        mask_image = np.zeros_like(image)
        for x0, y0, x1, y1 in lines:
            x0 = int(x0)
            y0 = int(y0)
            x1 = int(x1)
            y1 = int(y1)
            cv2.line(mask_image, (x0, y0), (x1, y1), color, thickness)

        # TODO Resmin altına çiziyor
        return cv2.addWeighted(image, 1, mask_image, 1, 0)

    def finding_center_point(image, lanes, new_image):
        nonlocal is_kawis
        nonlocal avg_slope

        height, width, _ = image.shape

        left_center_line = slope_to_point(
            height * 0.70,
            height * 0.75,
            avg_slope[0]
        )
        right_center_line = slope_to_point(
            height * 0.70,
            height * 0.75,
            avg_slope[1]
        )

        l0, l1, l2, l3 = left_center_line
        r0, r1, r2, r3 = right_center_line
        l0 = l2 = (l0 + l2) / 2
        r0 = r2 = (r0 + r2) / 2

        center_line = (
            (l0 + r0) / 2,
            l1,
            (l0 + r0) / 2,
            l3
        )

        left_center_line = l0, l1, l2, l3
        right_center_line = r0, r1, r2, r3

        # TODO HATA
        screen_center_line = (
            width / 2,
            center_line[3],
            width / 2,
            height
        )

        if width / 2 < center_line[0]:
            screen_horizontal_line = (
                screen_center_line[0],
                center_line[3],
                center_line[0],
                center_line[3]
            )

            center_sol_sag = 1

        else:
            screen_horizontal_line = (
                center_line[0],
                center_line[3],
                screen_center_line[0],
                center_line[3]
            )

            center_sol_sag = 0

        # Donuş çizgisinin uzunluğu
        center_donus_degeri = screen_horizontal_line[2] - \
            screen_horizontal_line[0]

        # TODO Kaldırılacak
        # Sağı görerek dönme
        m = n = 0
        if(lanes[1][0] != lanes[1][2]):  # egim infinite kontrolu
            m, n = np.polyfit((lanes[1][0], lanes[1][2]),
                              (lanes[1][1], lanes[1][3]), 1)

        # # print(f"--------- Egim: {m}, Kesişim {n}")

        # Sol çizgi yoksa
        if lanes[0][0] < -200 or (lanes[0][0] == 0 and lanes[0][2] == 0):
            left_center_line = (0, 0, 0, 0)
            center_line = (0, 0, 0, 0)
            screen_center_line = (0, 0, 0, 0)
            screen_horizontal_line = (0, 0, 0, 0)
            # center_donus_degeri = -1


            # print("Sag serit:", lanes[1][0] ,lanes[1][2])
            # Sağ çizgi varsa
            if lanes[1][0] > -200: #ters
                # Sağı görerek dönme
                m = n = 0
                ## print("lane0-2 :", lanes[1][0], lanes[1][2])
                if lanes[1][0] != lanes[1][2]:  # egim infinite kontrolu
                    m, n = np.polyfit(
                        (lanes[1][0], lanes[1][2]), (lanes[1][1], lanes[1][3]), 1)
                    ## print("m n :", m, n)
                if n > 25:
                    if m > 0.40 and m < 0.70:
                        center_sol_sag = 0
                        # TODO düzeltilecek
                        center_donus_degeri = 32 + n - 25
                else:  # Düz yol, sola yaklaş
                    is_kawis = 0

                    # print("Duzyol lanes:", lanes[1][2] , lanes[1][0])
                    if lanes[1][0] < width - 15:
                        # # print(
                        #    f"Düz yol sola yaklaş {lanes[1][2]} {width - 15}")
                        center_sol_sag = 0
                        center_donus_degeri = 40  # 5 * 8
                    else:  # Sağa yaklaş
                        center_sol_sag = 1
                        center_donus_degeri = 24  # 3 * 8
                if n > 45:
                    is_kawis = 99
                    center_sol_sag = 0
                    if n > 60:
                        center_donus_degeri = 104  # 10 * 8
                    else:
                        center_donus_degeri = 64  # 8 * 8
                    if m > 2:
                        center_donus_degeri = 120  # 8 * 15
                # print("donus degeri:", center_donus_degeri)

        elif lanes[1][0] < -200 or (lanes[1][0] == 0 and lanes[1][2] == 0):  # right x1 is null
            right_center_line = (0, 0, 0, 0)
            center_line = (0, 0, 0, 0)
            screen_center_line = (0, 0, 0, 0)
            screen_horizontal_line = (0, 0, 0, 0)
            # center_donus_degeri = -1

            if lanes[0][0] > -200:  # left.x1 is not null
                # TODO kavis için
                # Solu görerek dönme
                
                m = n = 0
                if lanes[0][0] != lanes[0][2]:  # egim infinite kontrolu
                    m, n = np.polyfit(
                        (lanes[0][0], lanes[0][2]), (lanes[0][1], lanes[0][3]), 1)
                if n > 25:
                    if m > 0.40 and m < 0.70:  # TODO degerler sol seritin egimine gore, saga gore duzeltilecek!!!
                        center_sol_sag = 1
                        # TODO düzeltilecek
                        center_donus_degeri = 32 + n - 25
                else:  # Düz yol, sola yaklaş
                    is_kawis = 0

                    # print("Duzyol SOLAAA:", lanes[0][0], lanes[0][2])
                    ## print("Duzyol SOLAAA:", lanes[0][0], lanes[0][2])
                    if lanes[0][0] > 15: #x1 > 0+15
                        # # print(
                        #    f"Düz yol saga yaklaş {lanes[0][0]} {width - 15}")
                        center_sol_sag = 1
                        center_donus_degeri = 40  # 5 * 8
                    else:  # Sağa yaklaş
                        center_sol_sag = 0
                        center_donus_degeri = 24  # 3 * 8
                if n > 45:
                    is_kawis = 99
                    center_sol_sag = 1
                    if n > 60:
                        center_donus_degeri = 104  # 10 * 8
                    else:
                        center_donus_degeri = 64  # 8 * 8
                    if m > 2:
                        center_donus_degeri = 120  # 8 * 15

        new_image = draw_lines(
            new_image,
            [
                left_center_line,
                right_center_line,
                center_line,
                screen_center_line,
                screen_horizontal_line
            ],
            color=[0, 255, 0],
            thickness=3
        )

        # sol sag 0 1 _ donus değeri
        return new_image, (center_sol_sag, center_donus_degeri)
    # try:
    copy_image = np.copy(image)
    copy_image = canny_img(copy_image)
    

    copy_image = region_of_interest(copy_image)
    #cv2.imshow("canny", copy_image)
    lines = hough_lines(copy_image)
    if lines is None:
        # print("none")
        return None  # Serit bulunamadiysa bir adim atla.
    avg_lines = avarage_lanes(copy_image, lines)
    copy_image = draw_lines(image, avg_lines)
    # center_sol_sag - center_donus_degeri
    # copy_image, donus_data = finding_center_point(image, avg_lines, copy_image)
    return finding_center_point(image, avg_lines, copy_image)
    # except:
    #    return -1
