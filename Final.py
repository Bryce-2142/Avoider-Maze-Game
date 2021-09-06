import sys, pygame, math,time

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames-1,10))
    for frame in range(number_of_frames):
        folder_and_file_name = str(sprite_folder_name) + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())
                             
    return frame_counts

# This function moves rect slowly between start_pos and end_pos. The num_frame parameter
# says how many frames of animation are needed to do the bounce, so a bigger number means
# the rect moves slower. frame_count is the current overall frame count from the game.
def bounce_rect_between_two_positions( rect, start_pos, end_pos, num_frame, frame_count ):
    if frame_count%num_frame < num_frame/2:
        new_pos_x = start_pos[0] + (end_pos[0] - start_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        new_pos_y = start_pos[1] + (end_pos[1] - start_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)
    else:
        new_pos_x = end_pos[0] + (start_pos[0] - end_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        new_pos_y = end_pos[1] + (start_pos[1] - end_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)

    rect.center = (new_pos_x, new_pos_y)

# The main loop handles most of the game    
def main():

    mapx = 2560
    mapy = 0
                             
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("1.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode((1225,650))
    
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    #clock = pygame.time.Clock()
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # create the hero character
    hero = load_piskell_sprite("hero",2)
    hero_rect = hero[0].get_rect()
    hero_rect.center = (50/2, 50/2)
    hero_move_x = 0
    hero_shots = []
    hero_shots_count = 0
    hero_max_shots = []

    #Bullet actions
    y_offset = 0
    for event in pygame.event.get():
        for i in range(0, 720, 2):
            if event.type == pygame.KEYDOWN:
                y_offset = 0
                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
                y_offset -= i
                laser_rect.y += y_offset
                print(y_offset)

    # create the enemy character
    enemy = load_piskell_sprite("enemy",2)
    enemy_rect = enemy[0].get_rect()
    enemy_rect.center = (50/2, 50/2)
    
    rect_list = []
    enemy_count = 0

    # create the laser bullets
    laser = load_piskell_sprite("laser",2)
    laser_rect = laser[0].get_rect()
    laser_rect.center = (20/2, 30/2)

    #Looping enemy rows and columns variables
    
    xoff = 5
    pixel_wide = 5

    points = 0

    running = True

    #create masks for color detection
    map_mask = pygame.mask.from_surface(map, 50)


    last_hx, last_hy = 0,0
    



#__________________________________________________________________________________________

    
    #Main Game Loop
        
    while is_alive:
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False


                   
                
        #Draw the screen
        screen.fill((255,255,255))
        screen.blit(map, map_rect)

        
        #Draw the rects
        #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
        #pygame.draw.rect(screen,(0,255,0), hero_rect, 3)

        #Attach hero's postion to mouse position
        pos = pygame.mouse.get_pos()
        hero_rect.center = (960, 590)
        laser_rect.center = pos
        laser_rect.y += y_offset
        #Load the sprite for animation
        laser_sprite = laser[frame_count%len(laser)]
        hero_sprite = hero[frame_count%len(hero)]
        enemy_sprite = enemy[frame_count%len(enemy)]

        hero_mask = pygame.mask.from_surface(hero_sprite, 50)

        #Offsets
        hx, hy = (hero_rect[0], hero_rect[1])
        off_x = hx - map_rect[0]
        off_y = hy - map_rect[1]

        #Overlaps
        overlap = map_mask.overlap(hero_mask, (off_x, off_y))
        last_hx, last_hy = hx, hy

        hero_rect.center = pos

        if overlap:
            game_over()

        #Draw the elements
        #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
        screen.blit(hero_sprite, hero_rect)
        #screen.blit(laser_sprite, laser_rect)
        screen.blit(enemy_sprite, enemy_rect)

        

        #Shooting Bullets
        laser_rect = laser[0].get_rect()
        laser_rect.center = pos
        #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##        for i in range(10):
##            if event.type == pygame.KEYDOWN:
##                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                y_offset -= 2
##                print(y_offset)
##                laser_rect.y += y_offset
##                screen.blit(laser_sprite, laser_rect)
##                screen.blit(map, map_rect)
##                laser_rect.y -= 2
##                laser_rect.centerx = pos[0]
##                laser_rect.y += i * -1
##                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                print("PRESSED")
            #screen.blit(laser_sprite, laser_rect)
               
##############################################################################
        #Enemy sweeping loop 1
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 50
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1
##############################################################################################
        #Enemy sweeping loop 2
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 200
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1

##############################################################################################
        #Enemy sweeping loop 3
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 350
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1

##############################################################################################
        #Enemy sweeping loop 4
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 500
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1
            
####################################################################################################

##        #Enemy sweeping loop 2
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 150
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
##
####        #Laser loop
####        for event in pygame.event.get():
####            if event.type == pygame.KEYDOWN:
####                laser_list = []
####                laser_rect_list = []
####                laser_count = 0
####                laser_rect = laser[0].get_rect()
####                laser_rect.center = pos
####                for i in range(pos[1] * -1 , 720, 2):
####                    laser_rect.y -= 2
####                    laser_list.append(laser_sprite)
####                    rect_list.append(pygame.draw.rect(screen,(255,0,0), laser_rect, 3))
####                    screen.blit(laser_list[laser_count], laser_rect)
####
####                    #Rect colliding code
####                    pygame.draw.rect(screen,(0,0,255), laser_rect, 2)
####                    if enemy_rect.colliderect(laser_rect):
####                       print("Colliding")
####                    else:
####                       print("Not Colliding")
####                       
####                    laser_count += 1



            
##            
##
##        #Enemy sweeping loop 3
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 250
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
##            
##
##        #Enemy sweeping loop 4
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 350
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
            

            

##        #Rect sweeping list
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128,1152,128):
##           enemy_rect[0] += i
##           enemy_rect.y = 50
##           pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##           if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##           else:
##               print("Not Colliding")
##           enemy_rect = enemy[0].get_rect()
        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())

        if pos[1] < 10:
            print("WINx1")
            lvl_2_int()
        

        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3
        
        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,255,0))
        screen.blit(label, (20,20))

        label2 = myfont.render("Points: " + str(points), True, (255,255,0))
        screen.blit(label2, (1000,20))

        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

        screen.blit(hero_sprite, hero_rect)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

#__________________________________________________________________________________________________________________

# Start the program

def intro():
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("start.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(map_size)
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # Loop while the player is still active
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        screen.blit(map, map_rect)

        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        if cursor_color == (0, 166, 81, 255):
            ins()
        if cursor_color == (166,0,0, 255):
           pygame.quit()
           sys.exit() 
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3

        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,200,0))
        screen.blit(label, (150,20))
        
        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def ins():
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("ins.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(map_size)
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # Loop while the player is still active
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        screen.blit(map, map_rect)

        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        if cursor_color == (0, 166, 81, 255):
            main()
        if cursor_color == (166,0,0, 255):
           pygame.quit()
           sys.exit() 
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3

        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,200,0))
        screen.blit(label, (150,20))
        
        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def lvl_2_int():
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("lvl2_start.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(map_size)
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # Loop while the player is still active
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        screen.blit(map, map_rect)

        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        if cursor_color == (0, 166, 81, 255):
            lvl_2()

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3

        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,200,0))
        screen.blit(label, (150,20))
        
        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def lvl_2():

    mapx = 2560
    mapy = 0
                             
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("2.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode((1225,650))
    
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    #clock = pygame.time.Clock()
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # create the hero character
    hero = load_piskell_sprite("hero",2)
    hero_rect = hero[0].get_rect()
    hero_rect.center = (50/2, 50/2)
    hero_move_x = 0
    hero_shots = []
    hero_shots_count = 0
    hero_max_shots = []

    #Bullet actions
    y_offset = 0
    for event in pygame.event.get():
        for i in range(0, 720, 2):
            if event.type == pygame.KEYDOWN:
                y_offset = 0
                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
                y_offset -= i
                laser_rect.y += y_offset
                print(y_offset)

    # create the enemy character
    enemy = load_piskell_sprite("enemy",2)
    enemy_rect = enemy[0].get_rect()
    enemy_rect.center = (50/2, 50/2)
    
    rect_list = []
    enemy_count = 0

    # create the laser bullets
    laser = load_piskell_sprite("laser",2)
    laser_rect = laser[0].get_rect()
    laser_rect.center = (20/2, 30/2)

    #Looping enemy rows and columns variables
    
    xoff = 5
    pixel_wide = 5

    points = 0

    running = True

    #create masks for color detection
    map_mask = pygame.mask.from_surface(map, 10)


    last_hx, last_hy = 0,0
    



#__________________________________________________________________________________________

    
    #Main Game Loop
        
    while is_alive:
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False


                   
                
        #Draw the screen
        screen.fill((255,255,255))
        screen.blit(map, map_rect)

        
        #Draw the rects
        #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
        #pygame.draw.rect(screen,(0,255,0), hero_rect, 3)

        #Attach hero's postion to mouse position
        pos = pygame.mouse.get_pos()
        hero_rect.center = (960, 590)
        laser_rect.center = pos
        laser_rect.y += y_offset
        #Load the sprite for animation
        laser_sprite = laser[frame_count%len(laser)]
        hero_sprite = hero[frame_count%len(hero)]
        enemy_sprite = enemy[frame_count%len(enemy)]

        hero_mask = pygame.mask.from_surface(hero_sprite, 50)

        #Offsets
        hx, hy = (hero_rect[0], hero_rect[1])
        off_x = hx - map_rect[0]
        off_y = hy - map_rect[1]

        #Overlaps
        overlap = map_mask.overlap(hero_mask, (off_x, off_y))
        last_hx, last_hy = hx, hy

        hero_rect.center = pos

##        if overlap:
##            game_over()

        #Draw the elements
        #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
        screen.blit(hero_sprite, hero_rect)
        #screen.blit(laser_sprite, laser_rect)
        screen.blit(enemy_sprite, enemy_rect)

        

        #Shooting Bullets
        laser_rect = laser[0].get_rect()
        laser_rect.center = pos
        #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##        for i in range(10):
##            if event.type == pygame.KEYDOWN:
##                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                y_offset -= 2
##                print(y_offset)
##                laser_rect.y += y_offset
##                screen.blit(laser_sprite, laser_rect)
##                screen.blit(map, map_rect)
##                laser_rect.y -= 2
##                laser_rect.centerx = pos[0]
##                laser_rect.y += i * -1
##                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                print("PRESSED")
            #screen.blit(laser_sprite, laser_rect)
               
##############################################################################
        #Enemy sweeping loop 1
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 50
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1
##############################################################################################
        #Enemy sweeping loop 2
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 200
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1

##############################################################################################
        #Enemy sweeping loop 3
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 350
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1

##############################################################################################
        #Enemy sweeping loop 4
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 500
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1
            
####################################################################################################

##        #Enemy sweeping loop 2
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 150
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
##
####        #Laser loop
####        for event in pygame.event.get():
####            if event.type == pygame.KEYDOWN:
####                laser_list = []
####                laser_rect_list = []
####                laser_count = 0
####                laser_rect = laser[0].get_rect()
####                laser_rect.center = pos
####                for i in range(pos[1] * -1 , 720, 2):
####                    laser_rect.y -= 2
####                    laser_list.append(laser_sprite)
####                    rect_list.append(pygame.draw.rect(screen,(255,0,0), laser_rect, 3))
####                    screen.blit(laser_list[laser_count], laser_rect)
####
####                    #Rect colliding code
####                    pygame.draw.rect(screen,(0,0,255), laser_rect, 2)
####                    if enemy_rect.colliderect(laser_rect):
####                       print("Colliding")
####                    else:
####                       print("Not Colliding")
####                       
####                    laser_count += 1



            
##            
##
##        #Enemy sweeping loop 3
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 250
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
##            
##
##        #Enemy sweeping loop 4
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 350
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
            

            

##        #Rect sweeping list
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128,1152,128):
##           enemy_rect[0] += i
##           enemy_rect.y = 50
##           pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##           if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##           else:
##               print("Not Colliding")
##           enemy_rect = enemy[0].get_rect()
        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())

        if pos[1] < 10:
            lvl_3_int()
        

        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3
        
        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,255,0))
        screen.blit(label, (20,20))

        label2 = myfont.render("Points: " + str(points), True, (255,255,0))
        screen.blit(label2, (1000,20))

        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

        screen.blit(hero_sprite, hero_rect)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def lvl_3_int():
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("lvl3_start.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(map_size)
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # Loop while the player is still active
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        screen.blit(map, map_rect)

        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        if cursor_color == (0, 166, 81, 255):
            lvl_3()

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3

        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,200,0))
        screen.blit(label, (150,20))
        
        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def lvl_3():

    mapx = 2560
    mapy = 0
                             
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("3.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode((1225,650))
    
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    #clock = pygame.time.Clock()
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # create the hero character
    hero = load_piskell_sprite("hero",2)
    hero_rect = hero[0].get_rect()
    hero_rect.center = (50/2, 50/2)
    hero_move_x = 0
    hero_shots = []
    hero_shots_count = 0
    hero_max_shots = []

    #Bullet actions
    y_offset = 0
    for event in pygame.event.get():
        for i in range(0, 720, 2):
            if event.type == pygame.KEYDOWN:
                y_offset = 0
                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
                y_offset -= i
                laser_rect.y += y_offset
                print(y_offset)

    # create the enemy character
    enemy = load_piskell_sprite("enemy",2)
    enemy_rect = enemy[0].get_rect()
    enemy_rect.center = (50/2, 50/2)
    
    rect_list = []
    enemy_count = 0

    # create the laser bullets
    laser = load_piskell_sprite("laser",2)
    laser_rect = laser[0].get_rect()
    laser_rect.center = (20/2, 30/2)

    #Looping enemy rows and columns variables
    
    xoff = 5
    pixel_wide = 5

    points = 0

    running = True

    #create masks for color detection
    map_mask = pygame.mask.from_surface(map, 10)


    last_hx, last_hy = 0,0
    



#__________________________________________________________________________________________

    
    #Main Game Loop
        
    while is_alive:
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False


                   
                
        #Draw the screen
        screen.fill((255,255,255))
        screen.blit(map, map_rect)

        
        #Draw the rects
        #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
        #pygame.draw.rect(screen,(0,255,0), hero_rect, 3)

        #Attach hero's postion to mouse position
        pos = pygame.mouse.get_pos()
        hero_rect.center = (960, 590)
        laser_rect.center = pos
        laser_rect.y += y_offset
        #Load the sprite for animation
        laser_sprite = laser[frame_count%len(laser)]
        hero_sprite = hero[frame_count%len(hero)]
        enemy_sprite = enemy[frame_count%len(enemy)]

        hero_mask = pygame.mask.from_surface(hero_sprite, 50)

        #Offsets
        hx, hy = (hero_rect[0], hero_rect[1])
        off_x = hx - map_rect[0]
        off_y = hy - map_rect[1]

        #Overlaps
        overlap = map_mask.overlap(hero_mask, (off_x, off_y))
        last_hx, last_hy = hx, hy

        hero_rect.center = pos

##        if overlap:
##            game_over()

        #Draw the elements
        #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
        screen.blit(hero_sprite, hero_rect)
        #screen.blit(laser_sprite, laser_rect)
        screen.blit(enemy_sprite, enemy_rect)

        

        #Shooting Bullets
        laser_rect = laser[0].get_rect()
        laser_rect.center = pos
        #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##        for i in range(10):
##            if event.type == pygame.KEYDOWN:
##                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                y_offset -= 2
##                print(y_offset)
##                laser_rect.y += y_offset
##                screen.blit(laser_sprite, laser_rect)
##                screen.blit(map, map_rect)
##                laser_rect.y -= 2
##                laser_rect.centerx = pos[0]
##                laser_rect.y += i * -1
##                pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                print("PRESSED")
            #screen.blit(laser_sprite, laser_rect)
               
##############################################################################
        #Enemy sweeping loop 1
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 50
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1
##############################################################################################
        #Enemy sweeping loop 2
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 200
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1

##############################################################################################
        #Enemy sweeping loop 3
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 350
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1

##############################################################################################
        #Enemy sweeping loop 4
        x_loc = 0
        enemy_list = []
        rect_list = []
        enemy_count = 0
        enemy_rect = enemy[0].get_rect()
        for i in range(128, 1152, 128):
            enemy_rect.x += 128
            enemy_rect.y = 500
            enemy_list.append(enemy_sprite)
            rect_list.append(enemy_rect)
            screen.blit(enemy_list[enemy_count], rect_list[enemy_count])

##            for i in range(0, 720, 2):
##                if event.type == pygame.KEYDOWN:
##                    y_offset = 0
##                    pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
##                    y_offset -= i
##                    laser_rect.y += y_offset
##                    screen.blit(laser_sprite, laser_rect)

            laser_rect = laser[0].get_rect()
            laser_rect.center = pos
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            for i in range(10):
                if event.type == pygame.KEYDOWN:
##                    if y_offset > -720:
##                        x_loc = pos[0]
##                        y_offset -= 1
##                        if y_offset == -720:
##                            y_offset = 0
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0
##                if event.type == pygame.KEYUP:
##                    if y_offset > -720:
##                        y_offset -= 1
##                        if x_loc != pos[0]:
##                            y_offset = 0
##                    else:
##                        y_offset = 0


                    laser_list = []
                    laser_rect_list = []
                    laser_count = 0
                    laser_rect = laser[0].get_rect()
                    laser_rect.center = pos
                    for i in range(pos[1] * -1 , 720, 360):
                        laser_rect.y -= 30
                        laser_list.append(laser_sprite)
                        #rect_list.append(pygame.draw.rect(screen,(0,0,255), laser_rect))
                        screen.blit(laser_list[laser_count], laser_rect)
                        screen.blit(hero_sprite, hero_rect)

                        #Rect colliding code
                        #pygame.draw.rect(screen,(0,0,255), laser_rect)
                        if rect_list[enemy_count].colliderect(laser_rect):
                           points += 1
##                    #pygame.draw.rect(screen, (0,0,255), laser_rect)
##                    pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##                    if enemy_rect.colliderect(laser_rect):
##                       print("Colliding")
                       

            #Rect colliding code
            #pygame.draw.rect(screen, (0,0,255), laser_rect, 2)
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if enemy_rect.colliderect(laser_rect):
                print("Shot Hit!")
                       
            #pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
            if hero_rect.colliderect(enemy_rect):
               game_over()
##            else:
##               print("Not Colliding")
               
            enemy_count += 1
            
####################################################################################################

##        #Enemy sweeping loop 2
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 150
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
##
####        #Laser loop
####        for event in pygame.event.get():
####            if event.type == pygame.KEYDOWN:
####                laser_list = []
####                laser_rect_list = []
####                laser_count = 0
####                laser_rect = laser[0].get_rect()
####                laser_rect.center = pos
####                for i in range(pos[1] * -1 , 720, 2):
####                    laser_rect.y -= 2
####                    laser_list.append(laser_sprite)
####                    rect_list.append(pygame.draw.rect(screen,(255,0,0), laser_rect, 3))
####                    screen.blit(laser_list[laser_count], laser_rect)
####
####                    #Rect colliding code
####                    pygame.draw.rect(screen,(0,0,255), laser_rect, 2)
####                    if enemy_rect.colliderect(laser_rect):
####                       print("Colliding")
####                    else:
####                       print("Not Colliding")
####                       
####                    laser_count += 1



            
##            
##
##        #Enemy sweeping loop 3
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 250
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
##            
##
##        #Enemy sweeping loop 4
##        enemy_list = []
##        rect_list = []
##        enemy_count = 0
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128, 1152, 128):
##            enemy_rect.x += 128
##            enemy_rect.y = 350
##            enemy_list.append(enemy_sprite)
##            rect_list.append(pygame.draw.rect(screen,(255,0,0), enemy_rect, 3))
##            screen.blit(enemy_list[enemy_count], enemy_rect)
##
##            #Rect colliding code
##            pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##            if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##            else:
##               print("Not Colliding")
##               
##            enemy_count += 1
            

            

##        #Rect sweeping list
##        enemy_rect = enemy[0].get_rect()
##        for i in range(128,1152,128):
##           enemy_rect[0] += i
##           enemy_rect.y = 50
##           pygame.draw.rect(screen,(255,0,0), enemy_rect, 3)
##           if hero_rect.colliderect(enemy_rect):
##               print("Colliding")
##           else:
##               print("Not Colliding")
##           enemy_rect = enemy[0].get_rect()
        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())

        if pos[1] < 10:
            print("SUCK")
            lvl_2()
        

        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3
        
        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,255,0))
        screen.blit(label, (20,20))

        label2 = myfont.render("Points: " + str(points), True, (255,255,0))
        screen.blit(label2, (1000,20))

        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

        screen.blit(hero_sprite, hero_rect)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def game_over():
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("game_over.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(map_size)
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # Loop while the player is still active
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        screen.blit(map, map_rect)

        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        if cursor_color == (0, 166, 81, 255):
            main()
        if cursor_color == (166,0,0, 255):
           pygame.quit()
           sys.exit() 
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3

        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,200,0))
        screen.blit(label, (150,20))
        
        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

######################################

def game_win():
    # Initialize pygame                                 
    pygame.init()

    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)

    # Load in the background image
    map = pygame.image.load("ins.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    map_rect = map.get_rect()
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(map_size)
        
    # The frame_count counts all the frames that have passed since the start of the game.
    # Look at the print statements in the loop to see how to use the count with a mod function
    # to get cycles of different lengths.
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # The game should not start until the start color is clicked. Until then game_started is False
    game_started = False

    # is_alive means that the game loop should continue. Winning or losing the game sets is_alive to False.
    is_alive = True

    # Loop while the player is still active
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        screen.blit(map, map_rect)

        # This grabs the current color under the cursor from the screen. Note that anything
        # drawn on the screen before this statement adds to the color. I could have also
        # taken the color from the map if I just wanted that.
        cursor_color = screen.get_at(pygame.mouse.get_pos())
        # Note that the color has 4 values - the 4th is alpha. If you want to compare colors
        # make sure that you compare all the values. An example would be
        # cursor_color == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        if cursor_color == (0, 166, 81, 255):
            main()
        if cursor_color == (166,0,0, 255):
           pygame.quit()
           sys.exit() 
        print("Color:", cursor_color)

        # You may have sprites with different numbers of frames. We can make cycles
        # of different lengths by using mod on the frame_count. This is easier than
        # maintaining a different frame count variable for each different sprite.
        print("Cycle of length 3:", frame_count%3) # counts 0,1,2,0,1,2
        print("Cycle of length 4:", frame_count%4) # counts 0,1,2,3,0,1,2,3

        # Render text to the screen
        label = myfont.render("By Rudy and Bryce!", True, (255,200,0))
        screen.blit(label, (150,20))
        
        # Bring drawn changes to the front
        pygame.display.update()

        # We are basically done this with frame of animation, so update the count.
        frame_count += 1

        # This tries to force the loop to run at 1/2 fps. The is artifically slow so the output above
        # can be inspected. You should change this speed. Something like 30 is more normal.
        clock.tick(10)

    # This happens once the loop is finished - the game is over.
    pygame.quit()
    sys.exit()

intro()

    
