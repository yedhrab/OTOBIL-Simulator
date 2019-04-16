import time

from PIL import Image

from pynput.keyboard import Controller as KController, Key
from pynput.mouse import Controller as MController, Button as MButton

# Similasyon içerisinde herhangi bir koordinat
POSITION = (40, 80)
# TODO Model üzerinden çalıştığında ona uygun verinin girilmesi lazım
# 90 derecelik dönüş için gereken zaman
# TURN_TIME = 1.48
# Dönüşte hız kaybını engellemek için verilen hız süresi
TURN_THROTTLE_TIME = 0.8
# Fare ile odaklandıktan sonra beklenen zaman
FOCUS_WAITING_TIME = 0.5
# Arabayı durdurmak için gereken süre
BREAK_TIME = 4

# ---------------------- #
#  Deneysel Değişkenler  #
# TODO    degiskenler    #
# SLEEP_TIME = 3.75
TURN_TIME = 1.41
UZUN_YOL_TIME = 9.23
KISA_YOL_TIME = 9.23
# ---------------------- #

# Kontrolcüleri ayarlama
keyboard = KController()
mouse = MController()


def __focus():
    """Sİmilasyona odaklanma
    Fare'yi similasyona getirir ve üzerine tıklar.
    Odaklanma olmadan tuş kombinasyonlarının gönderimi başarısız olur.
    """

    mouse.position = POSITION
    mouse.click(MButton.left)
    time.sleep(FOCUS_WAITING_TIME)


def __hold_key(key, sec=0.):
    keyboard.press(key)

    if sec > 0:
        time.sleep(sec)
        keyboard.release(key)


# TURN_TIME değişebilir
def turn(ratio: float, save_speed=True):
    """Aracın dönemsini sağlar
    Aracın dönüşünü, isteğe bağlı olarak hız kaybını engelleyerek sağlar

    Arguments:
        ratio {float} -- Dönüş değeri, `-1` sola 90 derece dönüş, `+1` sağa 90 derece dönüş anlamına gelir

    Keyword Arguments:
        save_speed {bool} -- Hızı koru (default: {True})
    """

    key = 'd' if ratio > 0 else 'a'
    # hold_key(key, TURN_TIME * abs(ratio))

    if save_speed:
        __hold_key(key, TURN_TIME * abs(ratio))
    else:
        keyboard.release('w')
        __hold_key(key, TURN_TIME * abs(ratio))
        keyboard.press('w')


# k ye basılıp basılmayacağına karar veren
def set_speed_limit(limit: bool):
    """20 Hız limitini aktif eder

    Arguments:
        limit {bool} -- `True` veya `False`
    """
    if limit:
        keyboard.press('k')
    else:
        keyboard.release('k')


# w ya basılı tutuyor
def move():
    """Similasyondaki aracın ilerlemesi
    Similasyonda manuel olarak 'w' tuşuna basma işlemini sağlar.

    Keyword Arguments:
        stable {bool} -- Sabit hızda gitme (default: {False})
    """
    __hold_key('w', 0)  # Hızı kesmeden ilerleme


# Aracı durdurup 3 saniye bekler
def stop():
    """
    Aracı durdurup 5 saniye bekler
    """
    keyboard.release('w')
    keyboard.press(Key.space)
    time.sleep(5)
    keyboard.release(Key.space)

# tıklayıp sürmeyi başlatır


def test_etrafindaBirTur():
    initiate()
    time.sleep(37)
    turn(-1)
    time.sleep(3.47)
    turn(-1)
    time.sleep(2.1)
    turn(-1)
    time.sleep(3.55)
    turn(-1)


def initiate():
    """Similasyonu başlatma
    Arabayı tam gazla hızlanacak şekilde similasyonu başlatır.
    """

    __focus()
    move()


def slow_down(ratio=1.):
    """Arabayı yavaşlatma
    Durak gibi alanlar görüldüğünde arabayı belli bir oranda yavaşlatma

    Keyword Arguments:
        ratio {float} -- Hız düşürme oranı (default: {1.})

    Examples:
        Oran `1` ise araba durur. `0.5` ise hız yarıya indirilir
    """

    keyboard.release('w')
    __hold_key(Key.space, BREAK_TIME * ratio)


def test_method(other_test):
    """Test metodlarını test eder
    Test metodlarını geçen süreyi ve adını yazarak test eder

    Arguments:
        other_test {function} -- Test metodu
    """

    first_time = time.time()
    other_test()
    print(f"'{other_test.__name__}' metodunda geçen süre: {time.time() - first_time}")


def first_part():
    """İlk parçayı test etme
    Başlangıçtan, ilk Girilmez levhasındaki dönüşe kadar olan kısmı ele alır.
    """

    initiate()
    time.sleep(4.9)
    slow_down(1)
    move()
    time.sleep(2.9)
    slow_down(1)
    move()
    time.sleep(2.35)
    turn(-0.755)


def test_second_part():
    time.sleep(3.8)
    turn(0.95)
    time.sleep(4.7)
    turn(-0.95)


def test_third_part():
    time.sleep(4.7)
    turn(-0.5)
    time.sleep(1)
    turn(-0.27)
    time.sleep(3.9)
    turn(-1)


def test_last_part():
    time.sleep(5.3)
    turn(1)
    time.sleep(5.7)
    stop()


def test_duraklarda_dur():
    time.sleep(4.74)
    stop()
    move()
    time.sleep(3.03)
    stop()


def test_sim():
    # Dediğim şekilde testleri `test_method` içerisinde kullanmamışsın 😟
    # 20 hız limitini ele almamışsın
    # Onun dışındakiler için teşekkürler güzel olmuş :)
    test_method(first_part)
    test_method(test_second_part)
    test_method(test_third_part)
    test_method(test_last_part)


# Doğrudan çalıştırılırsa testi aktif etme
if __name__ == "__main__":
    test_sim()
