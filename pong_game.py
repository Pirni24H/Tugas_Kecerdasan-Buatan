"""
Pong Game - Tkinter
Kontrol:
Player 1 : W / S
Player 2 : Panah Atas / Panah Bawah
"""

from tkinter import *
import random

WIDTH, HEIGHT = 900, 500
PAD_W, PAD_H = 12, 100
BALL_RADIUS = 15

INITIAL_SPEED = 6
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 18
PAD_SPEED = 18

BALL_X_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])
BALL_Y_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])

LEFT_SPEED = 0
RIGHT_SPEED = 0

P1_SCORE = 0
P2_SCORE = 0

root = Tk()
root.title("Pong Game")
root.resizable(False, False)

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.pack()

c.create_line(PAD_W,0,PAD_W,HEIGHT,fill="white")
c.create_line(WIDTH-PAD_W,0,WIDTH-PAD_W,HEIGHT,fill="white")
c.create_line(WIDTH/2,0,WIDTH/2,HEIGHT,fill="white",dash=(8,6))

ball = c.create_oval(WIDTH/2-BALL_RADIUS, HEIGHT/2-BALL_RADIUS,
                     WIDTH/2+BALL_RADIUS, HEIGHT/2+BALL_RADIUS,
                     fill="white")

left_pad = c.create_rectangle(20, HEIGHT/2-PAD_H/2,
                              32, HEIGHT/2+PAD_H/2,
                              fill="yellow")

right_pad = c.create_rectangle(WIDTH-32, HEIGHT/2-PAD_H/2,
                               WIDTH-20, HEIGHT/2+PAD_H/2,
                               fill="cyan")

p1_text = c.create_text(WIDTH/4,35,text="0",font=("Arial",24),fill="white")
p2_text = c.create_text(WIDTH*3/4,35,text="0",font=("Arial",24),fill="white")

def reset_ball(direction=1):
    global BALL_X_SPEED, BALL_Y_SPEED
    c.coords(ball,
             WIDTH/2-BALL_RADIUS, HEIGHT/2-BALL_RADIUS,
             WIDTH/2+BALL_RADIUS, HEIGHT/2+BALL_RADIUS)
    BALL_X_SPEED = INITIAL_SPEED * direction
    BALL_Y_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])

def update_score():
    c.itemconfig(p1_text,text=str(P1_SCORE))
    c.itemconfig(p2_text,text=str(P2_SCORE))

def bounce():
    global BALL_X_SPEED
    BALL_X_SPEED *= -1
    if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
        BALL_X_SPEED *= BALL_SPEED_UP

def key_press(e):
    global LEFT_SPEED, RIGHT_SPEED
    if e.keysym.lower()=="w":
        LEFT_SPEED=-PAD_SPEED
    elif e.keysym.lower()=="s":
        LEFT_SPEED=PAD_SPEED
    elif e.keysym=="Up":
        RIGHT_SPEED=-PAD_SPEED
    elif e.keysym=="Down":
        RIGHT_SPEED=PAD_SPEED

def key_release(e):
    global LEFT_SPEED, RIGHT_SPEED
    if e.keysym.lower() in ("w","s"):
        LEFT_SPEED=0
    elif e.keysym in ("Up","Down"):
        RIGHT_SPEED=0

def move_pads():
    for pad,speed in ((left_pad,LEFT_SPEED),(right_pad,RIGHT_SPEED)):
        c.move(pad,0,speed)
        x1,y1,x2,y2 = c.coords(pad)
        if y1<0:
            c.move(pad,0,-y1)
        elif y2>HEIGHT:
            c.move(pad,0,HEIGHT-y2)

def move_ball():
    global BALL_X_SPEED,BALL_Y_SPEED,P1_SCORE,P2_SCORE
    c.move(ball,BALL_X_SPEED,BALL_Y_SPEED)
    bx1,by1,bx2,by2 = c.coords(ball)
    cy=(by1+by2)/2

    if by1<=0 or by2>=HEIGHT:
        BALL_Y_SPEED*=-1

    lx1,ly1,lx2,ly2 = c.coords(left_pad)
    rx1,ry1,rx2,ry2 = c.coords(right_pad)

    if bx1<=lx2:
        if ly1<=cy<=ly2:
            bounce()
        else:
            P2_SCORE+=1
            update_score()
            reset_ball(1)

    if bx2>=rx1:
        if ry1<=cy<=ry2:
            bounce()
        else:
            P1_SCORE+=1
            update_score()
            reset_ball(-1)

def game_loop():
    move_pads()
    move_ball()
    root.after(20,game_loop)

c.focus_set()
c.bind("<KeyPress>",key_press)
c.bind("<KeyRelease>",key_release)

game_loop()
root.mainloop()
