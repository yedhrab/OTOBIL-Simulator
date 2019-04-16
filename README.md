# Simulator <!-- omit in toc -->

Teknofest - Robotaksi yarışması için OTOBIL ekibi tarafından kullanılan similasyon.

## İçerikler <!-- omit in toc -->

- [Komple Kullanım](#komple-kullan%C4%B1m)
- [Klasör Yapısı](#klas%C3%B6r-yap%C4%B1s%C4%B1)
- [Kod Notları](#kod-notlar%C4%B1)
- [Sim Kullanımı](#sim-kullan%C4%B1m%C4%B1)
- [Linux Notları](#linux-notlar%C4%B1)
- [Yapılacaklar](#yap%C4%B1lacaklar)
- [Olası Sorunlar](#olas%C4%B1-sorunlar)

## Komple Kullanım

- Tensorflow ortamınızın olduğundan emin olun yoksa kurun
- `pip install pynput` ile gerekli modülü ortamınıza yükleyin.
- Modelin `label_map.pbtx₺` dosyalarını ve `frozen_inference_graph.pb` dosyalarınızı `model` dizinine kopyalayın.
- Similatörün dizinine `cd` ile gelin.
  - `dir` yazdığınız `LICENSE`, `README.md` falan yazması lazım.
- `python src\custom_detection.py` ile test edebilirsiniz.

> Alan seçimini `ctrl_l` tuşuna basılı tutarak yapıyorsunuz.

## Klasör Yapısı

| Dosya                                              | Açıklama                                   |
| -------------------------------------------------- | ------------------------------------------ |
| [src\simulator.py](src\simulator.py)               | Simlasyona veri aktarma işlemleri          |
| [src\custom_detection.py](src\custom_detection.py) | Her şey hazır olduğunda kullanılacak dosya |
| [src\detection_utils.py](src\detection_utils.py)   | Modeli kullanarak algılama yardımcıları    |
| [deprecetad](deprecetad)                           | Eski çalışmalar                            |

## Kod Notları

| Kod                 | Açıklama                      |
| ------------------- | ----------------------------- |
| `time.sleep(<sec>)` | Verilen saniye kadar bekletme |

- `<sec>` Küsüratlı saniye
  - *Örn: 200ms = `0.2`, 1000ms = `1`, 1213ms = `1.213`*

## Sim Kullanımı

| Tuş                | Açıklama                   |
| ------------------ | -------------------------- |
| `w`, `a`, `s`, `d` | Yön tuşları                |
| `k`                | 20 hız limitini aktif etme |
| `space`            | Fren                       |

## Linux Notları

- Wine uygulamasını kurun
- `Winecfg` içerisinde `Graphic` ayarları içinde VM boyutlarını ayarlayın
- `wine Tekno...` ile exe dosyasını `Fullscreen` modda çalıştırın

> Aksi takdirde ekrandan ayrılındığında klavye yakalamayı kayıp etmekte

## Yapılacaklar

- [ ] Similasyonu kodlar ile istendiği gibi tamamlamak (Furkan Özbek)

## Olası Sorunlar

- [ ] Fren keskinliği gerekebilir.
- [ ] Fren'e basılı tutarken dönüşler yapılmıyor.