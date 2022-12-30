# pong_game.py

import pygame, sys

# initialization
clock = pygame.time.Clock()
pygame.init()

class Ball :
    def __init__(self, screen, color, posX, posY, radius) :
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show (self) :
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)
    def start_moving(self):
        self.dx = 2
        self.dy = 0.7
    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def paddle_collision(self) :
        self.dx = -self.dx

    def wall_collision(self):
        self.dy = - self.dy

    def restart_pos(self):
        self.posX = width // 2
        self.posY = height // 2
        self.dx = 0
        self.dy = 0
        self.show()




class Paddle :
    def __init__(self, screen, color, posX, posY, width, height ):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = "stopped"


        self.show()
    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))
    def move(self):
        if self.state == "up" :
            self.posY -= 1
        if self.state == "down" :
            self.posY += 1
    def clamp(self):
        if self.posY <= 0 :
            self.posY = 0
        if self.posY + self.height >= height :
            # self.posY  + self.height = height
            self.posY   = height - self.height

    def restart_pos(self):
        self.posY = height // 2 - self.height // 2
        self.state = "stopped"
        self.show()


class Score :
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold=True)
        self.label = self.font.render(self.points, 0, white)
        self.show()

    def show(self) :
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width //2 , self.posY))

    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, white)

    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, 0, white)


class CollisionManager :
    def between_ball_and_paddle1(self, ball, paddle1):
        if (ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height) and (ball.posX - ball.radius < paddle1.posX + paddle1.width):
            return True
        return False


    def between_ball_and_paddle2(self, ball, paddle2):
        if (ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height) and (ball.posX + ball.radius > paddle2.posX):
            return True
        return False

    def between_ball_and_walls(self, ball):
        # top
        if ball.posY - ball.radius <= 0 :
            return True
        # bottom
        if ball.posY + ball.radius >= height :
            return True
        return False

    def check_goal_player1(self, ball):
        return ball.posX - ball.radius >= width

    def check_goal_player2(self, ball):
        return ball.posX + ball.radius <= 0




width = 900
height = 500
height1 = 600

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height1))
pygame.display.set_caption("PONG GAME by sai kumar adapa ")

def paint_back() :
    screen.fill(black)
    pygame.draw.line(screen, white, (width//2, 0), (width//2, height), 5)
    pygame.draw.line(screen, white, (0, height), (width, height), 5)
    font = pygame.font.SysFont("monospace", 20, bold=True)
    moves = "E = Left_Up || D = Left_Down || I = Right_Up || K = Right_Down"
    instructions = "P = start the match || R = Reset the match"
    label = font.render(moves, 0, white)
    screen.blit(label, (15, height + 15))
    label = font.render(instructions, 0, white)
    screen.blit(label, (15, height + 45))
    label = font.render("-ask", 0, (0, 255, 0))
    screen.blit(label, (width - 57, height1 - 35))
def restart() :
    paint_back()
    score1.restart()
    score2.restart()
    ball.restart_pos()
    paddle1.restart_pos()
    paddle2.restart_pos()









paint_back()
# OBJECTS

ball = Ball(screen, white, width//2, height//2, 15)
paddle1 = Paddle(screen, white, 15, (height//2-120//2), 20, 120)
paddle2 = Paddle(screen, white, width-20-15, (height//2-120//2), 20, 120)
collision = CollisionManager()
score1 = Score(screen, '0',width//4, 15)
score2 = Score(screen, '0',width - width//4, 15)

# pygame.draw.line(screen, white, (15, (height//2-120//2)), (width-20-15, (height//2-120//2)), 5)


# VARIABLES
playing = False

# main loop
while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            sys.exit()

        if event.type == pygame.KEYDOWN :

            if event.key == pygame.K_ESCAPE:

                sys.exit()

            if event.key == pygame.K_p :
                ball.start_moving()
                playing = True


            if event.key == pygame.K_r :
                restart()
                playing = False

            if event.key == pygame.K_e :
                paddle1.state = "up"
            if event.key == pygame.K_d :
                paddle1.state = "down"
            if event.key == pygame.K_i:
                paddle2.state = "up"
            if event.key == pygame.K_k:
                paddle2.state = "down"

        if event.type == pygame.KEYUP :
            paddle1.state = "stopped"
            paddle2.state = "stopped"


    if playing :
        paint_back()
        ball.move()
        ball.show()


        paddle1.move()
        paddle1.clamp()
        paddle1.show()
        paddle2.move()
        paddle2.clamp()
        paddle2.show()

        # check for collision

        if collision.between_ball_and_paddle1(ball, paddle1) :
            ball.paddle_collision()
        if collision.between_ball_and_paddle2(ball, paddle2) :
            ball.paddle_collision()
        if collision.between_ball_and_walls(ball) :
            ball.wall_collision()

        if collision.check_goal_player1(ball) :
            paint_back()
            score1.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            playing = False
        if collision.check_goal_player2(ball) :
            paint_back()
            score2.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            playing = False

    score1.show()
    score2.show()
    clock.tick(400)


    pygame.display.update()
