import cv2
import numpy as np

# Открытие видеофайла
capture = cv2.VideoCapture('C:\\Users\\qwaly\\OneDrive\\desktop\\video\\videoo\\mp4.MP4')

# Проверка, удалось ли открыть видео
if not capture.isOpened():
    print("Ошибка: Не удалось открыть видео.")
    exit()

# Определяем параметры для записи видео
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Кодек для AVI
output_file = 'C:\\Users\\qwaly\\OneDrive\\desktop\\video\\output_video.avi'  # Путь к выходному файлу
fps = 30  # Частота кадров
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Создание объекта VideoWriter
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Проверка, удалось ли создать объект VideoWriter
if not out.isOpened():
    print("Ошибка: Не удалось создать VideoWriter.")
    exit()

angle = 0 
rotation_speed = 0.01  

while capture.isOpened():
    ret, frame = capture.read()

    if not ret:
        print("Ошибка: Не удалось прочитать кадр.")
        break

    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)

    # Центр кадра
    center_x, center_y = width // 3, height // 2

    # Смещение вершин для эффекта вращения
    offset_x = int(300 * np.sin(angle))
    offset_y = int(100 * np.cos(angle))

    # Перспективное преобразование для имитации 3D-поворота
    src_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    dst_points = np.float32([[offset_x, offset_y],
                             [width - offset_x, offset_y],
                             [width - offset_x, height - offset_y],
                             [offset_x, height - offset_y]])

    # Построение матрицы перспективного преобразования
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Применение перспективного преобразования
    rotated_frame = cv2.warpPerspective(frame, matrix, (width, height))

    # Преобразование кадра в оттенки серого
    gray_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2GRAY)

    # Показ результата
    cv2.imshow('Result', gray_frame)
    cv2.resizeWindow('Result', 1920, 1080)

    # Запись кадра в выходное видео
    out.write(rotated_frame)  # Записываем оригинальный повёрнутый кадр
    print("Кадр записан.")  # Отладочное сообщение

    # Увеличение угла для плавного вращения
    angle += rotation_speed  # Увеличиваем угол на каждый кадр

    # Выход из цикла при нажатии 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
capture.release()
out.release()  # Освобождаем объект VideoWriter
cv2.destroyAllWindows()

print("Запись завершена.")
