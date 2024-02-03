import cv2 as cv
import face_recognition as fr
import os
import time
from threading import Thread
from queue import Queue, Empty


def load_and_encode_images(folder_path, target_resolution=(640, 480)):
    known_faces = []
    known_names = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.jpg', '.png')):
            image_path = os.path.join(folder_path, file_name)
            img = fr.load_image_file(image_path)
            img = cv.resize(img, target_resolution)
            face_locations = fr.face_locations(img)

            if face_locations:
                face_encoding = fr.face_encodings(img, face_locations)[0]
                known_faces.append(face_encoding)
                known_names.append(os.path.splitext(file_name)[0])

    return known_faces, known_names


def detect_and_recognize_faces(frame, known_faces, known_names, result_queue):
    face_coordinates = None
    face_locations = fr.face_locations(frame)

    if len(face_locations) > 0:
        face_encodings = fr.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            face_coordinates = (left, top, right, bottom, name)

    result_queue.put(face_coordinates)


def main():
    start_time = time.time()
    print('Программа запущена')

    train_images_folder = 'media/images/train'
    known_faces, known_names = load_and_encode_images(train_images_folder)

    print(f"База лиц составлена за {time.time() - start_time} секунд")

    cap = cv.VideoCapture('media/videos/zoo.mp4')

    frame_count = 0
    fps = cap.get(cv.CAP_PROP_FPS) + 1 # fps в видео вывода
    delay_time = int(140 / fps) * 5 # Ожидание для нового кадра. Обратно fps
    print(fps, delay_time)

    result_queue = Queue()
    face_coordinates = None
    face_thread = None
    target_resolution = (1280, 720) # Разрешение для видео вывода
    no_face_count = 0
    no_face_attempts = 0 # Кол-во кадров без лица для удаления маски

    print(f"Перешли к распознаванию за {time.time() - start_time} секунд")

    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1

        if ret:
            # frame = cv.resize(frame, target_resolution)
            frame = cv.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            if face_thread is None or not face_thread.is_alive():
                face_thread = Thread(target=detect_and_recognize_faces, args=(frame, known_faces, known_names, result_queue))
                face_thread.start()

                try:
                    face_coordinates = result_queue.get_nowait()
                except Empty:
                    no_face_count += 1
                    if no_face_count == no_face_attempts:
                        face_coordinates = None
                        no_face_count = 0

            if face_coordinates:
                left, top, right, bottom, name = face_coordinates
                print(f'Рамка на {time.time() - start_time} секунде. На видео: {name}')
                cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 200), 4)
                cv.putText(frame, name, (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

            cv.imshow('Video', frame)

            if cv.waitKey(delay_time) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv.destroyAllWindows()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Программа выполнена за {execution_time} секунд")

if __name__ == "__main__":
    main()
