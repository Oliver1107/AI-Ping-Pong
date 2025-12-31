import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Ping Pong')

BG_COLOR = (0, 0, 0)

PADDLE_SIZE = (30, 200)
BALL_SIZE = 15

BALL_SPEED = 5


class Paddle:

    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed
    
    def draw(self, win):
        pygame.draw.rect(win, 'white', (self.x, self.y, *PADDLE_SIZE))
    
    def move(self, direction):
        movement = direction * self.speed

        if self.y - movement >= 0 and self.y - movement <= (HEIGHT - PADDLE_SIZE[1]):
            self.y -= movement
    
    def change_speed(self, change):
        self.speed += change


class Ball:

    def __init__(self, x, y, direction=[1,1]):
        self.x = x
        self.y = y
        self.direction = direction

    def draw(self, win):
        pygame.draw.circle(win, 'white', (self.x, self.y), BALL_SIZE)
    
    def move(self):
        self.x += self.direction[0] * BALL_SPEED
        self.y += self.direction[1] * BALL_SPEED
    
    def bounce(self, side):
        self.direction[side] *= -1


def draw(win, paddle1, paddle2, ball):
    win.fill(BG_COLOR)

    paddle1.draw(win)
    paddle2.draw(win)
    ball.draw(win)

def check_vertical_collision(paddle, ball):
    x_ = (paddle.x, paddle.x + PADDLE_SIZE[0])

    top_y = paddle.y - BALL_SIZE
    bottom_y = paddle.y + PADDLE_SIZE[1] + BALL_SIZE
    
    if ball.y in (top_y, bottom_y) and (ball.x >= x_[0] and ball.x <= x_[1]):
        return True

def check_side_collision(paddle, ball):
    y_ = (paddle.y, paddle.y + PADDLE_SIZE[1])

    left_x = paddle.x - BALL_SIZE
    right_x = paddle.x + PADDLE_SIZE[0] + BALL_SIZE
    
    if ball.x in (left_x, right_x) and (ball.y >= y_[0] and ball.y <= y_[1]):
        return True

def main():
    run = True
    Paddle1 = Paddle(100, 100)
    Paddle2 = Paddle(700, 100)
    Ball_ = Ball(WIDTH / 2, HEIGHT / 2)

    move_up = False
    move_down = False

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_up = True
                
                if event.key == pygame.K_DOWN:
                    move_down = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move_up = False
                
                if event.key == pygame.K_DOWN:
                    move_down = False

        if move_up:
            Paddle1.move(10)
        if move_down:
            Paddle1.move(-10)
        
        if Ball_.x == BALL_SIZE or Ball_.x == WIDTH - BALL_SIZE:
            Ball_.bounce(0)
        if Ball_.y == BALL_SIZE or Ball_.y == HEIGHT - BALL_SIZE:
            Ball_.bounce(1)
        
        if check_vertical_collision(Paddle1, Ball_):
            Ball_.bounce(1)
        if check_side_collision(Paddle1, Ball_):
            Ball_.bounce(0)

        Ball_.move()
        draw(WIN, Paddle1, Paddle2, Ball_)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
