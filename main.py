import os
import math
import random
import cv2
import numpy as np
from algo import get_game_status, findBestMove

player, opponent = 'X', 'O'


def draw_board_on_image(image, board):
    img_height, img_width = image.shape[:2]
    cell_height, cell_width = img_height // 3, img_width // 3
    output_image = image.copy()
    for i in range(1, 3):
        cv2.line(output_image, (0, i * cell_height), (img_width, i * cell_height), (0, 255, 0), 2)
        cv2.line(output_image, (i * cell_width, 0), (i * cell_width, img_height), (0, 255, 0), 2)
    for row in range(3):
        for col in range(3):
            center_x = int((col + 0.5) * cell_width)
            center_y = int((row + 0.5) * cell_height)
            if board[row][col] == 'X':
                offset = int(min(cell_height, cell_width) * 0.2)
                cv2.line(output_image,
                         (center_x - offset, center_y - offset),
                         (center_x + offset, center_y + offset),
                         (255, 0, 0), 2)
                cv2.line(output_image,
                         (center_x + offset, center_y - offset),
                         (center_x - offset, center_y + offset),
                         (255, 0, 0), 2)
            elif board[row][col] == 'O':
                radius = int(min(cell_height, cell_width) * 0.2)
                cv2.circle(output_image, (center_x, center_y), radius, (0, 0, 255), 2)

    return output_image


def draw_move_on_image(image, best_move, cell_height, cell_width, symbol='X', color=(51, 0, 25)):
    row, col = best_move
    center_x = int((col + 0.5) * cell_width)
    center_y = int((row + 0.5) * cell_height)

    if symbol == 'X':
        offset = int(min(cell_height, cell_width) * 0.1)
        cv2.line(image,
                 (center_x - offset, center_y - offset),
                 (center_x + offset, center_y + offset),
                 color, 15)
        cv2.line(image,
                 (center_x + offset, center_y - offset),
                 (center_x - offset, center_y + offset),
                 color, 15)
    elif symbol == 'O':
        radius = int(min(cell_height, cell_width) * 0.2)
        cv2.circle(image, (center_x, center_y), radius, color, 8)
    return image


def average_angle(line):
    x1, y1, x2, y2 = line
    angle = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
    return angle


def recognize_tic_tac_toe_board(image_path):
    image = cv2.imread(image_path)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=100, maxLineGap=20)

    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
        if abs(angle) < 30:
            horizontal_lines.append(line[0])

    selected_horizontal = horizontal_lines[0].tolist()
    avg_horizontal_angle = average_angle(selected_horizontal)
    rotation_angle = avg_horizontal_angle
    print(f"Angle for rotation: {rotation_angle:.2f}°")

    # Image rotation
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
    rotated = cv2.warpAffine(original, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(255, 255, 255))

    gray_rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    _, thresh_rotated = cv2.threshold(gray_rotated, 150, 255, cv2.THRESH_BINARY_INV)
    contours_rotated, _ = cv2.findContours(thresh_rotated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_image = rotated.copy()
    for contour in contours_rotated:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.drawContours(contours_image, [contour], -1, color, 3)
    scale_percent = 30
    resized_width = int(contours_image.shape[1] * scale_percent / 100)
    resized_height = int(contours_image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(contours_image, (resized_width, resized_height), interpolation=cv2.INTER_AREA)
    cv2.imshow('Contours with Random Colors', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img_height, img_width = rotated.shape[:2]
    cell_height, cell_width = img_height // 3, img_width // 3
    game_state = [["-" for _ in range(3)] for _ in range(3)]
    central_cell = []

    for contour in contours_rotated:
        area = cv2.contourArea(contour)
        if area < 500:
            continue

        x, y, w_box, h_box = cv2.boundingRect(contour)
        cv2.rectangle(rotated, (x, y), (x + w_box, y + h_box), (255, 255, 0), 5)

        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        if hull_area == 0:
            continue
        solidity = float(area) / hull_area

        # x,y is the top left corner
        center_x, center_y = x + w_box // 2, y + h_box // 2
        row, col = center_y // cell_height, center_x // cell_width

        if row < 0 or row >= 3 or col < 0 or col >= 3:
            continue

        if row == 1 & col == 1:
            central_cell.append(solidity)
        else:
            if solidity > 0.7:
                game_state[row][col] = "O"
            else:
                game_state[row][col] = "X"
        cv2.putText(rotated, f"{solidity:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 4)
        cv2.drawContours(rotated, [contour], -1, (0, 0, 255), 2)

    if len(central_cell) > 2:
        sorted_solidity = sorted(central_cell)
        second_min_solidity = sorted_solidity[1]
    elif len(central_cell) == 2:
        second_min_solidity = 0

    # central cell
    if second_min_solidity > 0.7:
        game_state[1][1] = "O"
    elif second_min_solidity == 0:
        game_state[1][1] = "-"
    else:
        game_state[1][1] = "X"

    print("State of the game:")
    for line in game_state:
        print("|".join(line))
    print(game_state)
    game_status = get_game_status(game_state)
    print(game_status)

    if game_status == "The game is still ongoing.":
        bestMove = findBestMove(game_state)
        print("The Optimal Move is :")
        print("ROW:", bestMove[0], " COL:", bestMove[1])

        rotated = draw_move_on_image(rotated, bestMove, cell_height, cell_width, symbol=player)

        image_1 = np.ones((300, 300, 3), dtype=np.uint8) * 255
        result_image = draw_board_on_image(image_1, game_state)
        best_move = (bestMove[0], bestMove[1])
        result_image = draw_move_on_image(result_image, best_move, 100, 100, symbol=player)

        cv2.imshow("Tic-Tac-Toe Board with Optimal Move", result_image)

    else:
        print("No move is necessary.")
        result_image = rotated
        cv2.putText(result_image, game_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    scale_percent = 30
    resized_width = int(rotated.shape[1] * scale_percent / 100)
    resized_height = int(rotated.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(rotated, (resized_width, resized_height), interpolation=cv2.INTER_AREA)

    cv2.imshow('Tic-Tac-Toe Board', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

    image_files.sort()

    print("List of images in the folder:")
    for i, filename in enumerate(image_files):
        print(f"{i + 1}: {filename}")

    choice = input("Enter the file number to process or 0 to process all: ")
    try:
        choice = int(choice)
    except ValueError:
        print("Error: input is not a number.")
        return
    if choice == 0:
        print("Processing all images...")
        for filename in image_files:
            image_path = os.path.join(folder_path, filename)
            recognize_tic_tac_toe_board(image_path)
    elif 1 <= choice <= len(image_files):
        filename = image_files[choice - 1]
        image_path = os.path.join(folder_path, filename)
        print(f"Processing file {filename}...")
        recognize_tic_tac_toe_board(image_path)
    else:
        print("Invalid choice. The entered number is out of the available file range.")


folder_path = './Tests'
process_images_in_folder(folder_path)
