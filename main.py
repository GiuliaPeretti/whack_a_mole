import pygame
from settings import *
import random
import numpy as np



def draw_background():
    screen.fill(BACKGROUND_COLOR)

def init_cell():
    cells=[]
    for i in range (size):
        t1=[]
        for j in range(size):
            t1.append({'difficulty':0, 'count': 0})
        cells.append(t1)
    return(cells)

def draw_grid():
    for i in range (20,581,cell_width):
        pygame.draw.line(screen, DARK_GRAY, (i,20),(i,580), 1)
        pygame.draw.line(screen, DARK_GRAY, (20,i),(580,i), 1)

    for i in range(len(COLORS)):
        pygame.draw.rect(screen, COLORS[i], (10*i,0,10,10))

def gen_buttons():
    x,y,w,h=640,20,100,30
    buttons=[]
    for i in range (1,6):
        buttons.append({'name': 'Level '+str(i), 'coordinates': (x,y,w,h)})
        y=y+h+10
    buttons.append({'name': 'Start', 'coordinates': (x,y,w,h)})
    y=y+h+10
    buttons.append({'name': 'Stop', 'coordinates': (x,y,w,h)})

    return(buttons)

def draw_buttons():
    for b in buttons:
        pygame.draw.rect(screen, GRAY, b['coordinates'])
        pygame.draw.rect(screen, BLACK, b['coordinates'], 3)
        text=font.render(b['name'], True, BLACK)
        screen.blit(text, (b['coordinates'][0]+10,b['coordinates'][1]+3))
    
    if selected!=-1:
        pygame.draw.rect(screen, PINK, buttons[selected]['coordinates'])
        pygame.draw.rect(screen, BLACK, buttons[selected]['coordinates'], 3)
        text=font.render(buttons[selected]['name'], True, BLACK)
        screen.blit(text, (buttons[selected]['coordinates'][0]+10,buttons[selected]['coordinates'][1]+3))

def get_cell_size():
    #56, 70, 80, 112, 140
    #10, 8, 7, 5, 4
    match selected:
        case 0:
            return(140, 560//140)
        case 1:
            return(112, 560//112)
        case 2:
            return(80, 560//80)
        case 3:
            return(70, 560//70)
        case 4:
            return(56, 560//56)

def draw_cell(row, col, color):
    x=col*cell_width+20+5
    y=row*cell_width+20+5
    pygame.draw.rect(screen, color, (x,y,cell_width-9,cell_width-9))

def gen_mole():
    difficulty=random.randint(1,5)
    row=random.randint(0,size-1)
    col=random.randint(0,size-1)
    while cells[row][col]['difficulty']!=0:
        row=random.randint(0,size-1)
        col=random.randint(0,size-1)
    draw_cell(row,col,COLORS[difficulty-1])
    cells[row][col]['difficulty']=difficulty
    cells[row][col]['count']=60-difficulty*10
    print(np.array(cells))

def cells_with_moles():
    moles=[]
    for row in range(len(cells)):
        for col in range(len(cells[row])):
            if cells[row][col]!=0:
                moles.append([row,col])
    return(moles)

def handle_cell_input(row, col):
    if cells[row][col]!=0:
        cells[row][col]=0
        score+=1

def display_score():
    font = pygame.font.SysFont('arial', 30)
    text=font.render('Scores: '+str(score), True, RED)
    screen.blit(text, (630,300))





if __name__=='__main__':

    pygame.init()
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
    pygame.display.set_caption('Whack a mole♥')
    font = pygame.font.SysFont('arial', 20)

    cell_width=560
    size=0
    selected = -1
    selected_game=-1
    score=0
    game_started = False
    run  = True
    draw_background()
    draw_grid()
    buttons=gen_buttons()
    draw_buttons()
    cells=init_cell()
    display_score()

    while run:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:
                x,y=pygame.mouse.get_pos()
                if(game_started and cell_width!=560 and x>=20 and x<=560 and y>=20 and y<=560):
                    col=(x-20)//cell_width
                    row=(y-20)//cell_width
                    handle_cell_input(row,col)
                else:
                    for i in range (len(buttons)):
                        if(x>=buttons[i]['coordinates'][0] and x<=buttons[i]['coordinates'][0]+buttons[i]['coordinates'][2] and y>=buttons[i]['coordinates'][1] and y<=buttons[i]['coordinates'][1]+buttons[i]['coordinates'][3]):
                            if(i<len(buttons)-2):
                                selected=i
                                game_started=False
                                draw_background()
                                draw_buttons()
                                cell_width, size=get_cell_size()
                                print(cell_width, size)
                                cells=init_cell()
                                print(np.array(cells))
                                draw_grid()
                                
                                break
                            elif(i==5):
                                print("start")
                                print(selected)
                                draw_buttons()
                                if game_started==False:
                                    selected_game=selected
                                    game_started=True
                            elif(i==6):
                                print("stop")
                                draw_buttons()

                                game_started=False
                    else:
                        selected=-1
                        draw_buttons()

        valid=cells_with_moles()
        for i in range(len(valid)):
            cells[valid[i][0]][valid[i][1]]['count']+=1
            
        pygame.display.flip()
        clock.tick(30)

    
    
    
    
    pygame.quit()