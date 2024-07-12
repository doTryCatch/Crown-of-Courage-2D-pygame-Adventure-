import pygame
import os
import sys,csv
from  Object import *
from Slidable import *
from Pushable import *
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tiles_dimension=(45,45)
enemy_size=(60,90)
CheckP=[]
img_arr=[]
tiles=[]
Slidables=[]
Ladder=[]
Food=[]
Door=[]
Lift=[]
Boxes=[]
Inventory=[]
Damage=[]
Pushables=[]
Danger=[]
Rest=[]
Floor=[]
Enemy=[]
By_product={"Boar":116,"Hyena":117,"Deceased":120,"Mummy":120,"Orc_Berserk":120,
            "Orc_Shaman":120,"Orc_Warrior":120}
Enemy_identity={451:"Boar",452:"Deceased",453:"Hyena",454:"Mummy",455:"Orc_Berserk"
                ,456:"Orc_Shaman",457:"Orc_Warrior",458:"Old_man",459:"",460:""}

identity={111:"Mushroom",112:"Mushroom",113:"Mushroom",114:"Mushroom",115:"Mushroom",
          116:"Meat",117:"Meat",118:"Meat",120:"Kit"}


def loadimages(path,tiles_dimension):
    img=pygame.image.load(path)
    img=pygame.transform.scale(img,tiles_dimension)
    return img




def load(index,range_i,array,img,dim):
    try:
        a=identity[index]
    except:
        a=""
    if img:
        if (90<index<=100):
            array.append(slideBlock(dim[0]*tiles_dimension[0],dim[1]*tiles_dimension[1],tiles_dimension[0],tiles_dimension[1],img))
        elif (210<index<=220):
            print(index)
            array.append(pushableObject(dim[0]*tiles_dimension[0],dim[1]*tiles_dimension[1],45,45,img))
        elif(range_i[0]<=index<=range_i[1]):
            array.append(objects(dim[0]*tiles_dimension[0],dim[1]*tiles_dimension[1],tiles_dimension[0],tiles_dimension[1],img,a))
        return array        
    else:
        if(range_i[0]<=index<=range_i[1]):
            array.append({"x":dim[0]*tiles_dimension[0],"y":dim[1]*tiles_dimension[1],"path":f"Assets/Enemies/{Enemy_identity[index]}",
                          "identity":Enemy_identity[index],"dimension":(150,150) if index==456 else (90,90)})
            
          
        return array   

def find_file_length(path):
    directory_path = "J:/Pygame Project/" + path
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    return  len(files)

def loadimages1(path):
    with open("Level12.csv") as file: 
        data = csv.reader(file)
        for all in data:
            tiles.append(all)
    hero_pos=()
    for i in range(len(tiles)):
       for j in range(len(tiles[0])):
            img=[]
            
            try:
                index=int(tiles[i][j])
                if(0<index<=90):
                    img.append(loadimages(f"{path}/Tile_{index}.png",tiles_dimension))
                    load(index,(0,90),Floor,img,(j,i))
                elif (90<index<=100):
                    img.append(loadimages(f"{path}/Tile_{index}.png",tiles_dimension))
                    load(index,(91,100),Slidables,img,(j,i))
                elif (100<index<=450):
                    try:
                        img.append(loadimages(f"{path}/Extras/Tile_{index}.png",tiles_dimension))
                    except:
                        for k in range(find_file_length(f"/Assets/Level1/1-2/Extras/Tile_{index}")):
                            img.append(loadimages(f"{path}/Extras/Tile_{index}/{k+1}.png",tiles_dimension))
                    
                    if 210<index<=220:
                        load(index,(211,220),Pushables,img,(j,i))
                    else:
                        load(index,(101,110),Ladder,img,(j,i))
                        load(index,(111,130),Food,img,(j,i))
                        load(index,(131,140),Door,img,(j,i))
                        load(index,(141,170),Lift,img,(j,i))
                        load(index,(171,180),Boxes,img,(j,i))
                        load(index,(181,200),Inventory,img,(j,i))
                        load(index,(201,210),Damage,img,(j,i))
                        load(index,(300,440),Rest,img,(j,i))
                        load(index,(441,450),CheckP,img,(j,i))
                  

                elif(index==0):
                    hero_pos=(j,i)
                
                else:
                    load(index,(451,460),Enemy,'',(j,i))
            except:
                img.append(pygame.image.load("Assets/Empty.png"))
            
    tiles[0][0]='-1'           
    return hero_pos,tiles,Floor, Slidables, Ladder, Food, Door, Lift, Boxes, Inventory, Damage, Pushables, Rest ,Enemy, CheckP      

##hero_pos_initial,tiles_arr_initial,tiles_initial,ladder_initial,food_initial,door_initial,lift_initial,boxes_initial,inventory_initial,others_initial,Enmy_initial=loadimages1('Assets/Level1/1-1')
hero_pos,tiles_arr,tiles,slidables,ladder,food,door,lift,boxes,inventory,damage,pushables,others,Enmy,CheckP=loadimages1('Assets/Level1/1-2')


def reload():
    hero_pos=hero_pos_initial
    tiles_arr=tiles_arr_initial
    tiles=tiles_initial
    ladder=ladder_initial
    food=food_initial
    door=door_initial
    lift=lift_initial
    boxes=boxes_initial
    inventory=inventory_initial
    others=others_initial
    Enmy=Enmy_initial





   


def loadimages2(path, Action, img_size):
    img_coll=[]
    len=find_file_length(f"{path}/{Action}")
  

    for i in range(len):
        img=pygame.transform.scale(pygame.image.load(f"{path}/{Action}/{Action}_{i}.png"),img_size)
        img_coll.append(img)
    return img_coll
            
def hover(array_of_setof_button_in_rect_form_with_pos):
        mouse_pos = pygame.mouse.get_pos()
        for img, position in array_of_setof_button_in_rect_form_with_pos:
            rect=img.get_rect(center=position)
            if rect.collidepoint(mouse_pos):
                # Adjust button's position and size for hover effect
                hovered_rect = pygame.Rect(
                    rect.left - 10,  # Move slightly left
                    rect.top - 10 ,   # Move upwards
                    rect.width + 15 , # Increase width
                    rect.height + 15 # Increase height
                )
                hovered_image = pygame.transform.scale(img, (hovered_rect.width, hovered_rect.height))
                screen.blit(hovered_image, hovered_rect)
            else:
                # Draw button without hover effect
                screen.blit(img, rect)    
def draw_rect( color,dimension):
    pygame.draw.rect(screen,color,dimension)
def Rect(img,pos):
    rect=img.get_rect(center=pos)
    return rect  
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
def blur_image(surface, radius):
    # Create a blurred copy of the surface using the average blur algorithm
    blurred_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    blurred_surface = pygame.transform.smoothscale(blurred_surface, (surface.get_width(), surface.get_height()))
    return blurred_surface  
def set_image(img,img_size): 
      Image = pygame.image.load(img) 
      Image = pygame.transform.scale(Image,img_size) if img_size else Image
      return Image

def load_conversation(file_name): 
    msg = []
    with open(file_name) as file:
        for line in file:
            msg.append(line)
    return msg

def print_text(text, pos, speaker):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, (0, 0, 0))  # Change to black (RGB values: 0, 0, 0)
    text_rect = text_surface.get_rect()

    padding = 10
    tail_offset = 20
    box_offset = 50

    if speaker == "player1":
        text_rect.topleft = (player1.x - tail_offset - text_rect.width, player1.y - text_rect.height - box_offset)
        tail_pos = (text_rect.right, text_rect.bottom)
        tail_end = (tail_pos[0] + tail_offset, tail_pos[1] + tail_offset)
    else:
        text_rect.topright = (player2.x + tail_offset + text_rect.width, player2.y - text_rect.height - box_offset)
        tail_pos = (text_rect.left, text_rect.bottom)
        tail_end = (tail_pos[0] - tail_offset, tail_pos[1] + tail_offset)

    background_rect = text_rect.inflate(padding, padding)
    
    pygame.draw.rect(screen, (245, 245, 220), background_rect)
    screen.blit(text_surface, text_rect)

    pygame.draw.polygon(screen, (245, 245, 220), [(tail_pos[0], tail_pos[1] - 5), 
                                          (tail_pos[0], tail_pos[1] + 5), 
                                          (tail_end[0], tail_end[1])])


##def check_collide(tiles, player, check_point):
##    x = player.x
##    y = player.y
##    if check_point == "left":
##        x = player.x - 4
##    elif check_point == "right":
##        x = player.x + 4
##    elif check_point == "up":
##        y = player.y - 4
##    elif check_point == "down":
##        y = player.y + 4
##    for all in tiles:
##        if pygame.Rect(x, y, player.width, player.height).colliderect(
##            pygame.Rect(all.x, all.y, all.width, all.height)
##        ):
##            return True
##
##    return False
