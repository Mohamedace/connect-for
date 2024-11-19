
import random
import time
from turtle import *


# Game state
turns = {'red': 'blue', 'blue': 'red'}
state = {
    'player': 'blue',
    'rows': [0] * 8,  # 8 columns now
    'board': [['' for _ in range(8)] for _ in range(9)],  # 9 rows now
    'score': {'red': 0, 'blue': 0},
}

# Player names (will be set by input)
player_names = {'red': '', 'blue': ''}

# Setup screen
screen = Screen()
screen.setup(420, 520, 370, 0)  # Adjusted for extra space for names
screen.bgcolor('black')  # Set background to black

def draw_stars():
    """Draw stars on the background for a starry effect."""
    penup()
    for _ in range(50):  # Draw 50 random stars
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        size = random.randint(1, 3)
        goto(x, y)
        dot(size, 'white')

def grid():
    """Draw the empty Connect Four grid."""
    penup()
    color('white')
    for row in range(9):
        for col in range(8):
            x = col * 50 - 200
            y = row * 50 - 250  # Lowered to avoid overlapping names
            goto(x, y)
            pendown()
            for _ in range(4):  # Draw a square
                forward(50)
                left(90)
            penup()

def draw_names():
    """Draw player names and their colors at the top."""
    penup()
    color('red')
    goto(-200, 220)  # Left side for red player
    dot(20, 'red')
    goto(-160, 210)
    write(f"{player_names['red']}:\nScore: {state['score']['red']}", font=("Arial", 14, "normal"))

    color('blue')
    goto(100, 220)  # Right side for blue player
    dot(20, 'blue')
    goto(140, 210)
    write(f"{player_names['blue']}:\nScore: {state['score']['blue']}", font=("Arial", 14, "normal"))
    update()

def check_win(player):
    """Check if the current player has connected four discs."""
    for row in range(9):
        for col in range(8):
            if state['board'][row][col] == player:
                # Check horizontal
                if col + 3 < 8 and all(state['board'][row][col + i] == player for i in range(4)):
                    highlight_discs(row, col, player, "horizontal")
                    return True
                # Check vertical
                if row + 3 < 9 and all(state['board'][row + i][col] == player for i in range(4)):
                    highlight_discs(row, col, player, "vertical")
                    return True
                # Check diagonal (bottom-left to top-right)
                if row + 3 < 9 and col + 3 < 8 and all(state['board'][row + i][col + i] == player for i in range(4)):
                    highlight_discs(row, col, player, "diag1")
                    return True
                # Check diagonal (top-left to bottom-right)
                if row - 3 >= 0 and col + 3 < 8 and all(state['board'][row - i][col + i] == player for i in range(4)):
                    highlight_discs(row, col, player, "diag2")
                    return True
    return False

def highlight_discs(row, col, player, direction):
    """Slowly change the winning discs to yellow."""
    for i in range(4):
        if direction == 'horizontal':
            x_pos = (col + i) * 50 - 200 + 25
            y_pos = row * 50 - 250 + 25
        elif direction == 'vertical':
            x_pos = col * 50 - 200 + 25
            y_pos = (row + i) * 50 - 250 + 25
        elif direction == 'diag1':
            x_pos = (col + i) * 50 - 200 + 25
            y_pos = (row + i) * 50 - 250 + 25
        elif direction == 'diag2':
            x_pos = (col + i) * 50 - 200 + 25
            y_pos = (row - i) * 50 - 250 + 25
        
        penup()
        goto(x_pos, y_pos)
        dot(40, 'yellow')  # Highlight winning discs in yellow
        update()
        time.sleep(0.5)  # Slow down the color change

def celebrate_win(player):
    """Display a message when a player wins a round."""
    penup()
    goto(0, 260)
    color(player)
    write(f"You won this round, {player_names[player]}!", align="center", font=("Arial", 20, "bold"))
    time.sleep(2)
    restart_game()

def celebrate_victory(player):
    """Display a final victory message when a player scores 3 points."""
    penup()
    clear()  # Clear previous drawings to focus on the victory message
    draw_stars()  # Keep stars as background
    grid()  # Show the grid in the background
    draw_names()  # Show player names and scores
    goto(0, 0)  # Position the victory message in the center
    color(player)
    write(f"Congratulations {player_names[player]}!", align="center", font=("Arial", 24, "bold"))
    update()  # Ensure the message appears
    time.sleep(3)  # Let the victory message stay for 3 seconds
    reset_game()


def draw_score():
    """Redraw the score area at the top."""
    clear()
    draw_stars()
    grid()
    draw_names()

def tap(x, y):
    """Draw red or blue circle in tapped column."""
    player = state['player']
    rows = state['rows']

    # Determine which column is clicked
    col = int((x + 200) // 50)
    if col < 0 or col >= 8:  # Out of bounds
        return
    row = rows[col]

    if row >= 9:  # The column is full
        return

    x_pos = col * 50 - 200 + 25
    y_pos = row * 50 - 250 + 25  # Adjusted for lowered grid

    penup()
    goto(x_pos, y_pos)
    dot(40, player)
    update()

    state['board'][row][col] = player
    rows[col] = row + 1

    if check_win(player):
        state['score'][player] += 1
        draw_score()
        
        if state['score'][player] == 3:
            celebrate_victory(player)
            return

        celebrate_win(player)
        return

    state['player'] = turns[player]

def restart_game():
    """Restart the game by resetting the game board but keeping the score."""
    state['board'] = [['' for _ in range(8)] for _ in range(9)]  # Reset the 9x8 grid
    state['rows'] = [0] * 8
    clear()
    draw_stars()
    grid()
    draw_names()

def reset_game():
    """Reset the game completely after one player wins."""
    state['score'] = {'red': 0, 'blue': 0}
    state['rows'] = [0] * 8
    state['board'] = [['' for _ in range(8)] for _ in range(9)]
    state['player'] = 'blue'
    clear()
    draw_stars()
    grid()
    draw_names()

# Get player names
player_names['red'] = screen.textinput("Player Name", "Enter the name of the red player:") or "Red Player"
player_names['blue'] = screen.textinput("Player Name", "Enter the name of the blue player:") or "Blue Player"

# Initialize the game
penup()
hideturtle()
tracer(False)
draw_stars()
grid()
draw_names()

screen.listen()
onscreenclick(tap)
done()
