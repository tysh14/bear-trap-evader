import pygame
from random import randint


class Bear_Face(pygame.sprite.Sprite):
    """Bear sprite that can be seen at the top of the game page"""
    
    def __init__(self):
        super().__init__()

        self.is_happy = False
        self.image = pygame.image.load('game_files/graphics/new_bear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))
        self.rect = self.image.get_rect(center = (425, 72.5))
    
    #Methods to change  bear image based on game state
    def unalive(self):
        self.image = pygame.image.load('game_files/graphics/sad_bear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))

    def make_happy(self):
        self.image = pygame.image.load('game_files/graphics/happy_bear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))
    
    def reset_bear(self):
        self.image = pygame.image.load('game_files/graphics/new_bear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))


class Grass_Tile(pygame.sprite.Sprite):
    """Grass tiles sprite for the main playing grid"""

    no_of_tiles = 0
    _column_pos = -1
    _row_pos = 0
    no_of_revealed_tiles = 0

    def __init__(self, trap_positions):
        super().__init__()

        Grass_Tile.no_of_tiles += 1
        Grass_Tile._column_pos += 1

        #changes row/column of tile accordingly
        if Grass_Tile._column_pos % 16 == 0 and Grass_Tile._column_pos != 0:
            Grass_Tile._row_pos += 1
            Grass_Tile._column_pos = 0

        #sets trap tiles
        if Grass_Tile.no_of_tiles in trap_positions:
            self.is_a_trap = True
        else:
            self.is_a_trap = False


        self.id = Grass_Tile.no_of_tiles
        self.row = Grass_Tile._row_pos
        self.column = Grass_Tile._column_pos
        self.is_revealed = False
        self.has_berry = False
        self.image_no = randint(0,1)
        self.image = pygame.image.load(f'game_files/graphics/grass{self.image_no}.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect(topleft = (25+(50*Grass_Tile._column_pos),145+(50*Grass_Tile._row_pos)))

    
    def reveal_tile(self,tile_group):
        """Returns False or True or None

        Based on whether player has clicked a trap tile, winning tile or
        any other type of tile respectively
        """


        if self.is_revealed == False and self.has_berry == False:
            self.is_revealed = True
            Grass_Tile.no_of_revealed_tiles +=1

            #If tile is a trap
            if self.is_a_trap == True:
                self.image = pygame.image.load('game_files/graphics/trap.jpg').convert_alpha()
                self.image = pygame.transform.scale(self.image,(50,50))
                return False

            #If tile is not a trap
            else:
                no_of_adj_traps = self.no_of_traps(tile_group)
                
                #Reveals the number of adjacent traps
                if no_of_adj_traps == 0:
                    self.image = pygame.image.load(f'game_files/graphics/dirt_tiles/bare_dirt{randint(0,1)}.jpg').convert_alpha()
                else:
                    self.image = pygame.image.load(f'game_files/graphics/dirt_tiles/dirt{no_of_adj_traps}.jpg').convert_alpha()

                self.image = pygame.transform.scale(self.image,(50,50))

                #If tile has no adjacent traps, call the zero-open method
                if no_of_adj_traps == 0:
                    reveal_tiles = get_zero_open_tiles(self,tile_group,[],[])
                    for tile in reveal_tiles:
                        Grass_Tile.no_of_revealed_tiles +=1
                        tile.image = pygame.image.load(f'game_files/graphics/dirt_tiles/bare_dirt{randint(0,1)}.jpg').convert_alpha()
                        tile.image = pygame.transform.scale(tile.image,(50,50)) 
                
                #If all non-trap tiles are revealed, win game
                if Grass_Tile.no_of_revealed_tiles == (256-35):
                    print("returned True")
                    return True

        return None
            


    def place_berry(self,score):
        """Returns the new score based on if a berry was added/removed (int)
        
        Changes self.image to add/remove berries onto/from a tile
        """

        #Adds a berry
        if self.is_revealed == False and self.has_berry == False:

            if score == 0:
                return score
            
            self.has_berry = True
            self.image = pygame.image.load(f'game_files/graphics/berries{self.image_no}.jpg').convert_alpha()
            self.image = pygame.transform.scale(self.image,(50,50))
            return score-1
        
        #Removes a berry
        elif self.is_revealed == False and self.has_berry == True:

            self.has_berry = False
            self.image = pygame.image.load(f'game_files/graphics/grass{self.image_no}.jpg').convert_alpha()
            self.image = pygame.transform.scale(self.image,(50,50))
            return score+1
        
        elif self.is_revealed == True:
            return score
        
    def no_of_traps(self,tile_group):
        """Returns the number of traps adjacent to a tile (int)"""

        counter = 0

        #Adjacent tile index list
        #[left,right,up,down,topleft,topright,bottomleft,bottomright]
        adj_tiles_index = [self.id-1-1,self.id+1-1, \
                            self.id-16-1,self.id+16-1, \
                            self.id-16-2, self.id-16, \
                            self.id+16-2,self.id+16]
        
        #Removes appropriate indeces from list if tile is at the edge of the grid
        if self.row == 0:
            adj_tiles_index.remove(self.id-16-1) #up
            adj_tiles_index.remove(self.id-16-2) #topleft
            adj_tiles_index.remove(self.id-16) #topright

        elif self.row == 15:
            adj_tiles_index.remove(self.id+16-1) #down
            adj_tiles_index.remove(self.id+16-2) #bottomleft
            adj_tiles_index.remove(self.id+16) #bottomright


        if self.column == 0:

            adj_tiles_index.remove(self.id-1-1) #left

            need_to_remove = [self.id+16-2,self.id-16-2] #bottomleft, topleft
            for index in need_to_remove: #checks if index was already removed
                if index in adj_tiles_index:
                    adj_tiles_index.remove(index)

        elif self.column == 15:
            adj_tiles_index.remove(self.id+1-1) #right
            
            need_to_remove = [self.id+16,self.id-16] #bottomright, topright
            for index in need_to_remove: #checks if index was already removed
                if index in adj_tiles_index:
                    adj_tiles_index.remove(index)


        for index in adj_tiles_index:
            if tile_group[index].is_a_trap:
                counter += 1
        
        return counter
    
    def reset_tile(self,trap_positions):
        """Resets all tile attributes to default and allocates new set of trap tiles"""
        
        self.is_revealed = False
        self.has_berry = False
        self.image_no = randint(0,1)
        self.image = pygame.image.load(f'game_files/graphics/grass{self.image_no}.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))

        if self.id in trap_positions:
            self.is_a_trap = True
        else:
            self.is_a_trap = False


def get_zero_open_tiles(curr_tile, tile_group,check_adj_q,tiles_to_reveal):
    """Returns a list of tile objects that need to be revealed in a 'zero-open'

    Recursive method which finds adjacent empty tiles when doing a 'zero-open'
    check_adj_q = queue of tiles where their surrounding tiles need to be checked if they're empty
    """

    #Removes head of queue
    if len(check_adj_q) != 0:
        del check_adj_q[0]

    #Surrounding indeces of a tile
    adj_tiles_index = [curr_tile.id-1-1,curr_tile.id+1-1,curr_tile.id-16-1,curr_tile.id+16-1]
    
    #Appropriate indeces are removed if curr_tile is at a grid boundary
    if curr_tile.row == 0:
        adj_tiles_index.remove(curr_tile.id-16-1)
    elif curr_tile.row == 15:
        adj_tiles_index.remove(curr_tile.id+16-1)

    if curr_tile.column == 0:
        adj_tiles_index.remove(curr_tile.id-1-1)
    elif curr_tile.column == 15:
        adj_tiles_index.remove(curr_tile.id+1-1)

    for index in adj_tiles_index:
        #Adjacent tile is revealed + added to queue if it has no adjacent traps, isn't a trap and is not yet revealed
        if tile_group[index].no_of_traps(tile_group) == 0 and tile_group[index].is_a_trap == False and tile_group[index].is_revealed == False:
            tile_group[index].is_revealed = True
            check_adj_q.append(tile_group[index])
            tiles_to_reveal.append(tile_group[index])

    if len(check_adj_q) != 0: 
        return get_zero_open_tiles(check_adj_q[0],tile_group,check_adj_q,tiles_to_reveal)
        #Next curr_tile is the head of the queue

    else:
        return tiles_to_reveal

