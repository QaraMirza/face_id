The program recognizes faces in video. If they have a photo of the person in the “media/images/train” folder, then the person will be in the database and will be tagged in the video. The directory for training images and videos can be changed in code. In order to display video from the computer camera, you need to change the line to cv.VideoCapture(0)

Libraries used:
- OpenCV
-face-recognition
- os
- time
- threading
- queue

The code is rendered slowly. I would be grateful for advice on optimizing and speeding up the program.

===================================================================================

Программа распознает лица на видео. Если они фотография лица есть в папке "media/images/train", то человек будет в базе данных и его отметят в видео. Каталог для тренировочных изображений и видео можно изменить в коде. Для того, чтобы выводилось видео с камеры компьютера, нужно изменить строку на cv.VideoCapture(0)

Использовались библиотеки:
- OpenCV
- face-recognition
- os
- time
- threading
- queue

Код обраюатывается медленно. Буду благодарен за советы по оптимизации и ускорению работы программы
