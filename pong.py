# pong

import sys
import math
import pygame
from random import randint, choice

# size of a window
WIDTH = 800
HEIGHT = 500

# ball
BALL_SPEED = 12
BALL_SIZE = 20
BALL_COLOR = (255, 255, 255)

# length of a racket
RACKET_LENGTH = int(HEIGHT / 5)

# racket for a player; swing speed, initial position and color
SWING = 9
RACKET1_SIZE = (10, int((HEIGHT - RACKET_LENGTH) / 2), 10, RACKET_LENGTH)
RACKET1_COLOR = (255, 255, 255)

# racket for AI; swing speed, initial position and color
AI_SWING = 5
RACKET2_SIZE = (WIDTH - 20, int((HEIGHT - RACKET_LENGTH) / 2), 10, RACKET_LENGTH)
RACKET2_COLOR = (255, 0, 0)

# size of a frame
FRAME_TOP_SIZE = (0, 0, WIDTH, 5)
FRAME_BOTTOM_SIZE = (0, HEIGHT - 5, WIDTH, 5)
FRAME_CENTER_SIZE = (int(WIDTH / 2 - 2), 0, 4, HEIGHT)
FRAME_LEFT_SIZE = (0, 0, 5, HEIGHT)
FRAME_RIGHT_SIZE = (WIDTH - 5, 0, 5, HEIGHT)

# color of a frame
FRAME_COLOR = (255, 255, 255)

# game itself
def main():
    # initialization, key interval, frame rate, setting a display and a title
    pygame.init()
    pygame.key.set_repeat(1, 6)
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong')

    # initialize speed of a ball
    speed = BALL_SPEED

    # initialize scores
    score1 = 0
    score2 = 0

    # initialize winning flags
    victory_1 = False
    victory_2 = False

    # font for scores
    score_font = pygame.font.Font(None, 36)

    # font for game ending message
    end_font = pygame.font.Font(None, 50)

    # message when a player wins
    message_win1 = end_font.render('You win!', True, (255, 255, 255))
    message_pos1 = message_win1.get_rect()
    message_pos1.centerx = int(WIDTH / 4)
    message_pos1.centery = int(HEIGHT / 2)

    # message when a player loses
    message_win2 = end_font.render('You lose...', True, (255, 255, 255))
    message_pos2 = message_win2.get_rect()
    message_pos2.centerx = int(WIDTH * 3 / 4)
    message_pos2.centery = int(HEIGHT / 2)

    # generate Rect objects of a ball and rackets
    ball = pygame.Rect(surface.get_rect().centerx, surface.get_rect().centery, BALL_SIZE, BALL_SIZE)
    racket1 = pygame.Rect(RACKET1_SIZE)
    racket2 = pygame.Rect(RACKET2_SIZE)

    # generate Rect objects of frames
    FRAME_top = pygame.Rect(FRAME_TOP_SIZE)
    FRAME_bottom = pygame.Rect(FRAME_BOTTOM_SIZE)
    FRAME_center = pygame.Rect(FRAME_CENTER_SIZE)
    FRAME_left = pygame.Rect(FRAME_LEFT_SIZE)
    FRAME_right = pygame.Rect(FRAME_RIGHT_SIZE)

    # release a ball at random(prevents releasing at an angle of 90 and 270 degrees)
    direction = choice([randint(50, 70), randint(110, 130), randint(230, 250), randint(290, 310)])

    # loop game
    while True:

        # score for a player
        score1_show = score_font.render('You: ' + str(score1), True, (255, 255, 255))
        score1_pos = score1_show.get_rect()
        score1_pos.centerx = int(WIDTH / 4)
        score1_pos.centery = 40

        # score for AI
        score2_show = score_font.render('Pong AI: ' + str(score2), True, (255, 255, 255))
        score2_pos = score2_show.get_rect()
        score2_pos.centerx = int(WIDTH * 3 / 4)
        score2_pos.centery = 40

        # key-binding for movements of a player
        # move when arrow keys are pressed
        # exit from a game when Esc or a quit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and racket1.top > 10:
                    racket1.centery += -SWING
                if event.key == pygame.K_DOWN and racket1.bottom < HEIGHT - 10:
                    racket1.centery += SWING
                if event.key == pygame.K_LEFT and racket1.left > 10:
                    racket1.centerx += -SWING
                if event.key == pygame.K_RIGHT and racket1.right < 100:
                    racket1.centerx += SWING
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # movements of AI
        # tries to move towards a ball
        # moves downward when AI-racket is above a ball
        # moves upward when AI-racket is below a ball
        # struggles when the ball is far, can't get to the ball easily
        if racket2.centery < ball.centery and racket2.bottom < HEIGHT - 5:
            racket2.centery += AI_SWING
            if racket2.centery < ball.centery - int(HEIGHT / 8) and ball.centerx > int(WIDTH / 2):
                racket2.centery += AI_SWING + randint(-3, 3)
        elif racket2.centery > ball.centery and racket2.top > 5:
            racket2.centery += -AI_SWING
            if racket2.centery > ball.centery + int(HEIGHT / 8) and ball.centerx > int(WIDTH / 2):
                racket2.centery += -(AI_SWING + randint(-3, 3))

        # a ball makes a reflect with an irregular angle and accelerates when it hits a racket
        if racket1.colliderect(ball):
            direction = -(racket1.centery - ball.centery) + randint(-20, 20)
            speed += 0.3
        if racket2.colliderect(ball):
            direction = 180 + (racket2.centery - ball.centery) + randint(-20, 20)
            speed += 0.1

        # a ball bounces and accelerates when it hits any frame
        if ball.centery < 0 or ball.centery > HEIGHT:
            direction = -direction
            speed += 0.2

        # a ball moves only inside a frame
        # scores when a player or AI failed to contact a ball
        # victory flag is up when one scores more than 10 points with advantage of two or more points
        if ball.centerx >= 0 and ball.centerx <= WIDTH:
            ball.centerx += int(math.cos(math.radians(direction)) * speed)
            ball.centery += int(math.sin(math.radians(direction)) * speed)
        else:
            if (score1 < 11 and score2 < 11) or (score1 >=11 and score1 < score2 + 2) or (score2 >= 11 and score2 < score1 + 2):
                if ball.centerx > WIDTH:
                    score1 += 1
                    ball.left = int(WIDTH / 2)
                    ball.top = int(HEIGHT / 2)
                    direction = choice([randint(50, 70), randint(110, 130), randint(230, 250), randint(290, 310)])
                    speed = BALL_SPEED
                if ball.centerx < 0:
                    score2 += 1
                    ball.left = int(WIDTH / 2)
                    ball.top = int(HEIGHT / 2)
                    direction = choice([randint(50, 70), randint(110, 130), randint(230, 250), randint(290, 310)])
                    speed = BALL_SPEED
            if score1 >= 11 and score1 >= score2 + 2:
                victory_1 = True
            if score2 >= 11 and score2 >= score1 + 2:
                victory_2 = True

        # paint a display with a color of real-life table tennis
        surface.fill('royalblue2')

        # depict a message when a player or AI wins
        if victory_1:
            surface.blit(message_win1, (message_pos1))
        if victory_2:
            surface.blit(message_win2, (message_pos2))

        # depict frames
        pygame.draw.rect(surface, FRAME_COLOR, FRAME_top)
        pygame.draw.rect(surface, FRAME_COLOR, FRAME_bottom)
        pygame.draw.rect(surface, FRAME_COLOR, FRAME_center)
        pygame.draw.rect(surface, FRAME_COLOR, FRAME_left)
        pygame.draw.rect(surface, FRAME_COLOR, FRAME_right)

        # depict scores
        surface.blit(score1_show, (score1_pos))
        surface.blit(score2_show, (score2_pos))

        # depict rackets
        pygame.draw.rect(surface, RACKET1_COLOR, racket1)
        pygame.draw.rect(surface, RACKET2_COLOR, racket2)

        # depict a ball
        pygame.draw.ellipse(surface, BALL_COLOR, ball)

        # update a display, fix frame rate at 60fps
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
