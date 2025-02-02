# 🎮 Tic-Tac-Toe Game with Image Recognition 🧠🔍

This project is a **Tic-Tac-Toe** game that uses **image recognition** to detect the current state of the game board from an image. It also includes a **minimax algorithm** to determine the optimal move for the player. 🚀

## ✨ Features

- ✅ **Recognizes** the Tic-Tac-Toe board from an image 📸  
- ✅ **Detects** the current state of the game 🔍  
- ✅ Uses the **Minimax algorithm** to find the best move 🤖  
- ✅ **Draws** the game board and the optimal move on the image 🎨

## 📌 Requirements

- 🐍 Python 3.12  
- 📷 OpenCV  
- 🔢 NumPy

## 🔧 Installation

1️⃣ **Clone the repository:**

    git clone https://github.com/sofibrezden/TicTacToe-OpenCV.git
    cd TicTacToe-OpenCV

2️⃣ **Install the required packages:**

    pip install -r requirements.txt


## Usage

1️⃣ **Run the `main.py` script:**

    python main.py


2️⃣ **Follow the prompts to select an image to process.**


## 📂 Project Structure

- 📜`algo.py`: Contains the minimax algorithm and game evaluation functions.
- 📜`main.py`: Contains the main logic for image recognition and game processing.
- 📁`Tests`: Folder to store the images of Tic-Tac-Toe boards.

## 🛠️ Functions

### 🧩 algo.py

- `isMovesLeft(board)`: Checks if there are any moves left on the board.
- `evaluate(board)`: Evaluates the board and returns a score.
- `minimax(board, depth, isMax)`: Minimax algorithm to find the best move.
- `get_game_status(board)`: Returns the current status of the game.
- `findBestMove(board)`: Finds the best move for the player.

### 🎨 main.py

- `draw_board_on_image(image, board)`: Draws the Tic-Tac-Toe board on the image.
- `draw_move_on_image(image, best_move, cell_height, cell_width, symbol, color)`: Draws the optimal move on the image.
- `average_angle(line)`: Calculates the average angle of a line.
- `recognize_tic_tac_toe_board(image_path)`: Recognizes the Tic-Tac-Toe board from an image.
- `process_images_in_folder(folder_path)`: Processes all images in the specified folder.

## 📜License

This project is licensed under the MIT License. See the `LICENSE` file for details.