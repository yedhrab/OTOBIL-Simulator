import time

import cv2
import numpy as np

import simulator as sim
from image_processing_utils import *
from screen_utils import capture_screenshot, draw_dimension

# Yeni ekran görüntüsünü alma tekniği
NEW_SS_MODE = True

# Hata ayıklama ve bilgilendirme notlarını aktif eder
DEBUG = True

# Çıktı kaydını aktif etmeden
KEEP = False
SHOW = True

# İşlemleri seçmek için sabitlerd
SIM_INITIATE = True  # S
MODEL_ACTIVE = True  # Tensorflow modelini aktif etmea
LABEL_SWITCH_ACTIVE = True  # Algılanan etiketlere göre tepkileri aktif eder
IMAGE_PROCESSING_ACTIVE = True  # Görüntü işlemeyi aktif etme
TEST_LINE_ACTIVE = False  # Geçici test satırı

# Yakalanan ekranın gösterilme boyutu (Varsayılan için 0 yapıwd n)
WIDTH = 0
HEIGHT = 0

SIGN_SIZE = 18

if not NEW_SS_MODE:
    from PIL import ImageGrab as ig

if DEBUG:
    frame_count = 0
    last_time = time.time()

DIMENSION = (0, 45, 800, 670)  # (1, 40, 600, 440) # draw_dimension()

print(f'Seçilen alan: {DIMENSION}')

OUT = cv2.VideoWriter(
    'OUTput.avi',
    cv2.VideoWriter_fourcc(*'XVID'),
    5.0,
    (DIMENSION[2] - DIMENSION[0], DIMENSION[3] - DIMENSION[1])
) if KEEP else None


if MODEL_ACTIVE:
    from detection_utils import detect_from_image, is_model_prepared, prepare_tf_model
    prepare_tf_model()

is_durak = False
is_finishing = False
sim_initated = False
turn_count = 0
while True:
    if NEW_SS_MODE:
        # Ekran görüntüsü
        SCREEN = capture_screenshot(DIMENSION)
        SCREEN_NP_RGB = np.copy(SCREEN)
        SCREEN_NP_RGB = SCREEN_NP_RGB[:, :, 0:3]
    else:
        SCREEN = ig.grab(DIMENSION)
        SCREEN_NP = np.copy(SCREEN)
        # BGR tipindeki görüntüyü RGB yapıyoruz
        SCREEN_NP_RGB = cv2.cvtColor(SCREEN_NP, cv2.COLOR_BGR2RGB)

    if TEST_LINE_ACTIVE:
        # if is_stop_point(SCREEN_NP_RGB):
        #     print("------------------------ DUR -----------------------")  # BOZUK
        # print(should_car_turn(SCREEN_NP_RGB))
        # print(detect_turn_direction(SCREEN_NP_RGB))  # Çalışıyor
        # from detection_utils import detect_from_image
        # DETECT_INFOS = detect_from_image(SCREEN_NP_RGB, visualize=True)
        # for label, koordinate in DETECT_INFOS:
        #     if label in (1, 3):
        #         print((koordinate[2] - koordinate[0]))
        pass

    if IMAGE_PROCESSING_ACTIVE:
        # TODO Önce opencv sonra model işleme. OpenCV modeli etkilemez
        # ? görüntü işleme resmin kopyasında mı yapılmalı
        IMAGE_PROCESS_DATA = find_turn_angle(SCREEN_NP_RGB)
        if IMAGE_PROCESS_DATA is not None:
            SCREEN_NP_RGB, angle_data = IMAGE_PROCESS_DATA

            # TODO vakit kalırsa bakılacak
            # Sola dönüş
            if angle_data[0] == 0:
                turn_rate = angle_data[1] / 1500
                sim.turn(-turn_rate)
            # Sağa dönüş
            else:
                turn_rate = angle_data[1] / 1500
                sim.turn(turn_rate)

    if MODEL_ACTIVE:
        if not is_durak:
            # Ekranda algılama yapma ve işaretleme
            DETECT_INFOS = detect_from_image(SCREEN_NP_RGB, visualize=True)

            # Levhalara göre tepkiler
            for label, koordinate in DETECT_INFOS:
                # dur +
                if label == 1:
                    # Kırmızıya uzak lazım
                    # Durak veya bitis çizgisi true dönerse durd
                    # 7'den daha uzun olursa yaklaşmışız demektir
                    if koordinate[2] - koordinate[0] > 7:
                        sim.slow_down()
                # durak +
                elif label == 2:
                    # çizgiye uzaklız lazım
                    # Durak veya bitis çizgisi true dönerse dur
                    size = koordinate[2] - koordinate[0]
                    print("Durak", size)
                    if size > 15:
                        sim.slow_down()
                        sim.move()
                        time.sleep(1)

                    # is_durak = True
                # gec +
                elif label == 3:
                    sim.move()
                # giris_yasak
                elif label == 4:
                    # -1 0 1 şeklinde veriler alınır
                    #  -1 -->{Sola döndürür}
                    #  0 -->{Tepki yok}
                    #  1 -->{Sağa döndürür}
                    # Fonksiyondan dönücek olan ratio değeri {-1, 0 veya 1}
                    # Dönüş değerini alıp dönmesi gereken zamanı kontrol eder ve döner
                    print("Giriş yasak")
                    turn_count += 1
                    ratio = detect_turn_direction(SCREEN_NP_RGB)
                    # if should_car_turn(SCREEN_NP_RGB):
                    if koordinate[2] - koordinate[0] > SIGN_SIZE and turn_count > 2:
                        time.sleep(0.45)
                        sim.turn(-0.755)  # sim.turn(ratio)
                        turn_count = 0
                # hiz_otuz ?
                elif label == 5:
                    # Gereksiz sanki :D 😁
                    pass
                # hiz_yirmi +
                elif label == 6:
                    # Hız 20 ye sabitlenir
                    sim.set_speed_limit(True)
                # park !
                # TODO
                elif label == 7:
                    pass
                # park_yasak !
                # TODOa
                elif label == 8:
                    pass
                # sag_ileriden
                elif label == 9:
                    # Mecburi sağ
                    # belirli bir zaman geçmesi gerekiyor
                    # Furkan'ın fonksiyonlar iş görmez burada
                    print("Sağ İleriden", koordinate[2] - koordinate[0])
                    turn_count += 1
                    if koordinate[2] - koordinate[0] > SIGN_SIZE * 0.7 and turn_count > 2:
                        time.sleep(1.05)
                        sim.turn(0.75)  # sim.turn(ratio)
                        turn_count = 0
                    pass
                # sag_yasak
                elif label == 10:
                    # Sağa dönüş yasak bu sebeple ya düz ilerler ya da sola döner
                    # Gitmesi gereken yola karar verir
                    # Furkan'ın fonksiyonlar iş görmez burada
                    pass
                # sol_ileriden
                elif label == 11:
                    # Mecburi sol
                    # belirli bir zaman geçmesi gerekiyor
                    # Furkan'ın fonksiyonlar iş görmez burada
                    print("Sol İleriden", koordinate[2] - koordinate[0])
                    turn_count += 1
                    if koordinate[2] - koordinate[0] > SIGN_SIZE and turn_count > 1:
                        time.sleep(0.85)
                        sim.turn(-0.65)  # sim.turn(ratio)
                        turn_count = 0
                    pass
                # sol_yasak
                elif label == 12:
                    # Sola dönüş yasak bu sebeple ya düz ilerler ya da sağa döner
                    # Gitmesi gereken yola karar verir
                    # Furkan'ın fonksiyonlar iş görmez burada
                    is_finishing = True
                # trafige_kapali
                elif label == 13:
                    # Araç düz devam edemez
                    # Görüntü işlenmesi gerekir veya detect_turn_direction çağırılabilir
                    # -1 0 1 şeklinde veriler alınır
                    #  -1 -->{Sola döndürür}
                    #  0 -->{Tepki yok}
                    #  1 -->{Sağa döndürür}
                    # Fonksiyondan dönücek olan ratio değeri {-1, 0 veya 1}
                    # Dönüş değerini alıp dönmesi gereken zamanı kontrol eder ve döner
                    print("trafiğe kapalı")
                    ratio = detect_turn_direction(SCREEN_NP_RGB)
                    if koordinate[2] - koordinate[0] > SIGN_SIZE:
                        time.sleep(0.4)
                        sim.turn(ratio)  # ? Tam -1
                # yirmi_son
                elif label == 14:
                    # Hız tekrar max(30) a dayanır
                    sim.set_speed_limit(False)

        # if is_durak:
        #     print("Dur?:", is_stop_point(SCREEN_NP_RGB))
        #     if is_stop_point(SCREEN_NP_RGB):
        #         sim.slow_down()
        #         sim.move()
        #         time.sleep(1.5)
        #         is_durak = False
        #         turn_count = 0
        if is_finishing and is_finishing_line(SCREEN_NP_RGB):
            sim.slow_down()

    # Gösterilecek ekranın boyutunu ayarlama
    SCREEN_WIDTH = WIDTH if WIDTH != 0 else DIMENSION[2] - DIMENSION[0]
    SCREEN_HEIGHT = HEIGHT if WIDTH != 0 else DIMENSION[3] - DIMENSION[1]

    # Sonucu videoya kayıt etme veye ekrana basma
    OUT.write(SCREEN_NP_RGB) if KEEP else None

    # Gösterme
    cv2.imshow(
        'object detection',
        cv2.resize(
            SCREEN_NP_RGB,
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )
    ) if SHOW else None

    # 'q' tuşuna basıldığında çıkma işlemi
    if cv2.waitKey(25) & 0xFF == ord('q'):
        OUT.release() if KEEP else None
        cv2.destroyAllWindows()
        break

    if SIM_INITIATE and not sim_initated:
        time.sleep(3)
        sim.initiate()
        sim_initated = True
        time.sleep(1)

    # FPS'yi gösterme
    if DEBUG:
        frame_count += 1
        if time.time() - last_time >= 1:
            print('FPS: {}'.format(frame_count))
            frame_count = 0
            last_time = time.time()
