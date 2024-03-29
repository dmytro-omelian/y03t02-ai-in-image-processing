import cv2
import numpy as np


def draw_lines(img, lines, color=[255, 0, 0], thickness=7):
    x_bottom_pos = []
    x_upper_pos = []
    x_bottom_neg = []
    x_upper_neg = []

    y_bottom = 540
    y_upper = 315

    for line in lines:
        for x1, y1, x2, y2 in line:
            if 0.5 < ((y2 - y1) / (x2 - x1)) < 0.8:
                slope = ((y2 - y1) / (x2 - x1))
                b = y1 - slope * x1

                x_bottom_pos.append((y_bottom - b) / slope)
                x_upper_pos.append((y_upper - b) / slope)

            elif -0.5 > ((y2 - y1) / (x2 - x1)) > -0.8:

                slope = (y2 - y1) / (x2 - x1)
                b = y1 - slope * x1

                x_bottom_neg.append((y_bottom - b) / slope)
                x_upper_neg.append((y_upper - b) / slope)

    lines_mean = np.array(
        [[int(np.mean(x_bottom_pos)), int(np.mean(y_bottom)), int(np.mean(x_upper_pos)), int(np.mean(y_upper))],
         [int(np.mean(x_bottom_neg)), int(np.mean(y_bottom)), int(np.mean(x_upper_neg)), int(np.mean(y_upper))]]

    )
    for i in range(len(lines_mean)):
        cv2.line(img, (lines_mean[i, 0], lines_mean[i, 1]), (lines_mean[i, 2], lines_mean[i, 3]), color, thickness)


def process_image(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)

    low_t, high_t = 50, 150
    edges = cv2.Canny(blur, low_t, high_t)

    vertices = np.array([
        [
            (0, img.shape[0]), (450, 310),
            (490, 310), (img.shape[1], img.shape[0])
        ]
    ], dtype=np.int32)

    mask = np.zeros_like(edges)
    ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_edges = cv2.bitwise_and(edges, mask)

    rho = 3
    theta = np.pi / 180
    threshold = 15
    min_line_len = 150
    max_line_gap = 60
    lines = cv2.HoughLinesP(
        masked_edges, rho, theta, threshold,
        np.array([]),
        minLineLength=min_line_len,
        maxLineGap=max_line_gap
    )
    try:
        draw_lines(img, lines)
    except:
        print("error...")


video_capture = cv2.VideoCapture('./resources/road.mp4')
while video_capture.isOpened():
    ret, frame = video_capture.read()
    if ret:
        process_image(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

video_capture.release()
cv2.destroyAllWindows()
