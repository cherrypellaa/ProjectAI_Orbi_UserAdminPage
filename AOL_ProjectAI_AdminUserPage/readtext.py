import cv2
import easyocr
import pyttsx3

reader = easyocr.Reader(['en'], gpu=False, verbose=False)
engine = pyttsx3.init()
engine.setProperty('rate', 150)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

print("Tekan 'c' untuk capture dan deteksi teks. Tekan 'q' untuk keluar.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca kamera.")
            break

        cv2.imshow('Tekan "c" untuk Capture dan Deteksi Teks', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            captured_frame = frame.copy()

            results = reader.readtext(captured_frame)
            spoken_texts = set()

            for bbox, text, score in results:
                if score > 0.25:
                    top_left = tuple([int(val) for val in bbox[0]])
                    bottom_right = tuple([int(val) for val in bbox[2]])

                    cv2.rectangle(captured_frame, top_left, bottom_right, (0, 255, 0), 2)
                    cv2.putText(captured_frame, text, (top_left[0], top_left[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    if text not in spoken_texts:
                        print(f"Membaca: {text}")
                        engine.say(text)
                        engine.runAndWait()
                        spoken_texts.add(text)

            cv2.imshow("Hasil Deteksi", captured_frame)
            cv2.waitKey(0)
            cv2.destroyWindow("Hasil Deteksi")

        elif key == ord('q'):
            print("Keluar...")
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    engine.stop()
