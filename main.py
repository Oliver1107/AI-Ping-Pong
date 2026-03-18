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

        if self.y + movement >= 0 and self.y + movement <= (HEIGHT - PADDLE_SIZE[1]):
            self.y += movement
    
    def change_speed(self, change):
        self.speed += change


class Ball:

    def __init__(self, x, y, direction=None):
        self.x = x
        self.y = y
        self.direction = direction or [1, 1]

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

def collide(paddle, ball):
    paddle_rect = pygame.Rect(paddle.x, paddle.y, *PADDLE_SIZE)
    ball_rect = pygame.Rect(ball.x-BALL_SIZE, ball.y-BALL_SIZE, BALL_SIZE*2, BALL_SIZE*2)
    return paddle_rect.colliderect(ball_rect)

def is_left_of_diagonal(paddle_x, paddle_y, change_x, change_y, ball):
    cross = (change_x) * (ball.y - paddle_y) - (change_y) * (ball.x - paddle_x)
    return cross <= 0

def is_right_of_diagonal(paddle_x, paddle_y, change_x, change_y, ball):
    cross = (change_x) * (ball.y - paddle_y) - (change_y) * (ball.x - paddle_x)
    return cross >= 0

def vertical_collision(paddle, ball):
    if ball.y < paddle.y:
        if (is_right_of_diagonal(paddle.x, paddle.y, -BALL_SIZE, -BALL_SIZE, ball) and 
            is_left_of_diagonal(paddle.x + PADDLE_SIZE[0], paddle.y, BALL_SIZE, -BALL_SIZE, ball)):
            return True
    elif ball.y > (paddle.y + PADDLE_SIZE[1]):
        if (is_left_of_diagonal(paddle.x, paddle.y + PADDLE_SIZE[1], -BALL_SIZE, BALL_SIZE, ball) and 
            is_right_of_diagonal(paddle.x + PADDLE_SIZE[0], paddle.y + PADDLE_SIZE[1], BALL_SIZE, BALL_SIZE, ball)):
            return True
    return False

def horizontal_collision(paddle, ball):
    if ball.x < paddle.x:
        if (is_left_of_diagonal(paddle.x, paddle.y, -BALL_SIZE, -BALL_SIZE, ball) and 
            is_right_of_diagonal(paddle.x, paddle.y + PADDLE_SIZE[1], -BALL_SIZE, BALL_SIZE, ball)):
            return True
    elif ball.x > (paddle.x + PADDLE_SIZE[0]):
        if (is_right_of_diagonal(paddle.x + PADDLE_SIZE[0], paddle.y, BALL_SIZE, -BALL_SIZE, ball) and 
            is_left_of_diagonal(paddle.x + PADDLE_SIZE[0], paddle.y + PADDLE_SIZE[1], BALL_SIZE, BALL_SIZE, ball)):
            return True
    return False

def push_ball_vert(paddle, ball):
    midpoint = paddle.y + (PADDLE_SIZE[1] / 2)

    if ball.y < midpoint:
        ball.y = paddle.y - BALL_SIZE - 1
    elif ball.y > midpoint:
        ball.y = paddle.y + PADDLE_SIZE[1] + BALL_SIZE + 1

def push_ball_horiz(paddle, ball):
    midpoint = paddle.x + (PADDLE_SIZE[0] / 2)

    if ball.x < midpoint:
        ball.x = paddle.x - BALL_SIZE - 1
    elif ball.x > midpoint:
        ball.x = paddle.x + PADDLE_SIZE[0] + BALL_SIZE + 1

def main():
    clock = pygame.time.Clock()
    run = True
    Paddle1 = Paddle(100, 100)
    Paddle2 = Paddle(700, 100)
    Ball_ = Ball(WIDTH / 2, HEIGHT / 2)

    move_up = False
    move_down = False

    while run:

        clock.tick(60)
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
        
        if collide(Paddle1, Ball_):
            if vertical_collision(Paddle1, Ball_):    
                Ball_.bounce(1)
                move_up = False
                move_down = False
                push_ball_vert(Paddle1, Ball_)
            if horizontal_collision(Paddle1, Ball_):
                Ball_.bounce(0)
                push_ball_horiz(Paddle1, Ball_)

        if move_up:
            Paddle1.move(-10)
        if move_down:
            Paddle1.move(10)
        
        if Ball_.x <= BALL_SIZE:
            Ball_.x = BALL_SIZE
            Ball_.bounce(0)
        if Ball_.x >= WIDTH - BALL_SIZE:
            Ball_.x = WIDTH - BALL_SIZE
            Ball_.bounce(0)
        if Ball_.y <= BALL_SIZE:
            Ball_.y = BALL_SIZE
            Ball_.bounce(1)
        if Ball_.y >= HEIGHT - BALL_SIZE:
            Ball_.y = HEIGHT - BALL_SIZE
            Ball_.bounce(1)

        Ball_.move()
        draw(WIN, Paddle1, Paddle2, Ball_)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
