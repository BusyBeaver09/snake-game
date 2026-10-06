import asyncio
import pygame
import random
import sys

pygame.init()

GRID_SIZE = 20
GRID_COUNT = 20
WINDOW_SIZE = GRID_SIZE * GRID_COUNT

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

BACKGROUND_COLOR = (30, 30, 40)
SNAKE_COLOR = (46, 204, 113)
FOOD_COLOR = (231, 76, 60)

snake_body = [[5, 10], [4, 10], [3, 10]]
snake_direction = "RIGHT"


def spawn_food():
    """Return a grid position that is not occupied by the snake."""
    available_positions = [
        [x, y]
        for x in range(GRID_COUNT)
        for y in range(GRID_COUNT)
        if [x, y] not in snake_body
    ]
    return random.choice(available_positions) if available_positions else None


food_position = spawn_food()
running = True

async def main():
    global snake_direction, food_position, running
    end_message = ""
    while running:
        frame_started = pygame.time.get_ticks()
        # Process each queued event exactly once.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key in (pygame.K_UP, pygame.K_w)
                        and snake_direction != "DOWN"):
                    snake_direction = "UP"
                elif (event.key in (pygame.K_DOWN, pygame.K_s)
                      and snake_direction != "UP"):
                    snake_direction = "DOWN"
                elif (event.key in (pygame.K_LEFT, pygame.K_a)
                      and snake_direction != "RIGHT"):
                    snake_direction = "LEFT"
                elif (event.key in (pygame.K_RIGHT, pygame.K_d)
                      and snake_direction != "LEFT"):
                    snake_direction = "RIGHT"

        if not running:
            break

        # Advance the snake once per frame, not once per input event.
        head_x, head_y = snake_body[0]
        if snake_direction == "UP":
            head_y -= 1
        elif snake_direction == "DOWN":
            head_y += 1
        elif snake_direction == "LEFT":
            head_x -= 1
        else:  # RIGHT
            head_x += 1

        new_head = [head_x, head_y]

        if not (0 <= head_x < GRID_COUNT and 0 <= head_y < GRID_COUNT):
            end_message = "Game Over: You hit the wall!"
            break

        # The tail is removed below when no food is eaten, so moving into the
        # current tail square is allowed and is not a self-collision.
        eating_food = new_head == food_position
        body_to_check = snake_body if eating_food else snake_body[:-1]
        if new_head in body_to_check:
            end_message = "Game Over: You bit yourself!"
            break

        snake_body.insert(0, new_head)
        if eating_food:
            food_position = spawn_food()
            if food_position is None:
                end_message = "You win: The board is full!"
                break
        else:
            snake_body.pop()

        screen.fill(BACKGROUND_COLOR)

        if food_position is not None:
            food_rect = pygame.Rect(
                food_position[0] * GRID_SIZE,
                food_position[1] * GRID_SIZE,
                GRID_SIZE - 2,
                GRID_SIZE - 2,
            )
            pygame.draw.rect(screen, FOOD_COLOR, food_rect)

        for segment in snake_body:
            segment_rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 2,
                GRID_SIZE - 2,
            )
            pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)

        pygame.display.flip()
        # Preserve the original 100 ms step while allowing browser events/rendering.
        elapsed = (pygame.time.get_ticks() - frame_started) / 1000
        await asyncio.sleep(max(0, 0.1 - elapsed))


    if sys.platform == "emscripten" and end_message:
        # The original writes to a terminal; show the same outcome in the webplayer.
        font = pygame.font.Font(None, 25)
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 145, WINDOW_SIZE, 105))
        for text, y in [(end_message, 180), ("Refresh the page to play again.", 215)]:
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=(WINDOW_SIZE // 2, y)))
        pygame.display.flip()
        await asyncio.sleep(0)
    else:
        if end_message:
            print(end_message)
        pygame.quit()


asyncio.run(main())
