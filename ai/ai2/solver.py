#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
import math
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems           

# NOTE: got rid of (x, y) from adjacent and made bad_stuff >= 3 instead of 2
def deadlock_detector(state, unstored_boxes):     
  x, y = state.width, state.height
  corners = ((0, 0), (0, y - 1), (x - 1, 0), (x - 1, y - 0))
  edges = ((0, x - 1), (0, y - 1))

    # or boxes_deadlock(state, box, edges)):
  for box in state.boxes:
    if box not in state.storage:
      # if(corner_deadlock_ob(state, box) 
      #    or edge_deadlock(state, box, edges) 
      #    or ooo_baby_this_is_bad(state, edges, unstored_boxes) 
      #    or boxes_deadlock(state, box, edges)): # is boxes_deadlock even helping lolz
      if VERY_BAD(state, box):
        return True

  return False

# NOTE: corner deadlock can occur between corner, corner or wall, obstacle or obstacle, obstacle, all those pairs 
# consider this:
#     /1/
# /2/BOX/3/        
#    /4/
# if 1, 3 are a 
# adj_1, adj_2, adj_3, and adj_4 based off this

# first hard code this
def VERY_BAD(state, box):
  x, y = box[0], box[1]
  adj_1, adj_2, adj_3, adj_4 = (x, y-1), (x-1, y), (x+1, y), (x, y+1) # chart above
  
  # if len(state.obstacles == 0) its empty but like doesn't take too much time to check i think?
  
  # now check if by a wall and theres no free storage 
  on_vert_wall = vert_wall_lock = box[0] == 0 or box[0] == state.width - 1
  on_hor_wall = hor_wall_lock = box[1] == 0 or box[1] == state.height - 1 
  
  # makes result worse by one
  on_vert_obs = vert_obs_lock = adj_2 in state.obstacles or adj_3 in state.obstacles
  on_hor_obs = hor_obs_lock = adj_1 in state.obstacles or adj_4 in state.obstacles
    
  empty = True
  
  ##################################################################
  if on_vert_wall or on_hor_wall:
    for storage in state.storage: 
      if box != storage: # this box is not in this spot already
        
        for other_box in state.boxes: #check if storage already taken
          if other_box == storage:
            empty = False
        
        if(empty):
          if (on_vert_wall) and storage[0] == box[0]: 
            vert_wall_lock = False
          if (on_hor_wall) and storage[1] == box[1]: 
            hor_wall_lock = False
        
        empty = True
                    
    if(vert_wall_lock or hor_wall_lock ): # if one is true, then a lock exists
      return True
  
  #------------CORNERS------------
  # corner of (1, 3), wall or obstacle
  if (adj_1 in state.obstacles or box[1] == 0) and (adj_3 in state.obstacles or box[0] == state.width - 1):
    return True
  
  # corner of (2, 4), wall or obstacle
  if (adj_2 in state.obstacles or box[0] == 0) and (adj_4 in state.obstacles or box[1] == state.height - 1):
    return True
  
  #------------SIDE BY SIDE ON A WALL
  if ((box[0] == 0 or box[0] == state.width - 1) and (adj_1 in state.boxes or adj_4 in state.boxes)):
    return True
  
  # boxes side by side horizontally while by a wall/by an obstacle
  if ((box[1] == 0 or box[1] == state.height - 1) and (adj_2 in state.boxes or adj_3 in state.boxes)):
    return True
  
  #------------SIDE BY SIDE BY AN OBSTACLE
  
  
  # -----------DUMP
  # if ((box[0] == 0 or adj_2 in state.obstacles or box[0] == state.width - 1 or adj_3 in state.obstacles) and (adj_1 in state.boxes or adj_4 in state.boxes)):
  #   return True
  
  # # boxes side by side horizontally while by a wall/by an obstacle
  # if ((box[1] == 0 or adj_1 in state.obstacles or box[1] == state.height - 1 or adj_4 in state.obstacles) and (adj_2 in state.boxes or adj_3 in state.boxes)):
  #   return True
  
  
  return False;

def corner_deadlock(state, box, corners):
  return box in corners

# check for if on an edge and two boxes next to each other 
def boxes_deadlock(state, box, edges):  
  x, y = box[0], box[1]
  box_adj_hor = ((x-1, y), (x+1, y))
  box_adj_vert = ((x, y+1), (x, y-1))
  
  on_hor_edge = box[0] in edges[0]  # check if its on an edge
  on_vert_edge = box[1] in edges[1]
  
  if on_hor_edge: #check if there are boxes horizontal to it
    for adj in box_adj_hor:
      if adj in state.boxes:
        return True
    
  if on_vert_edge: #check if there are boxes vertical to it
    for adj in box_adj_vert:
      if adj in state.boxes:
        return True
      
  return False

def get_adjacent(x, y):
  return ((x, y-1), (x-1, y), (x, y), (x+1, y),(x, y+1)) # NOTE: bro (X,Y) IS A MISTAKE WHY TF DOES IT SOLVE MORE W IT

def ooo_baby_this_is_bad(state, edges, unstored_boxes):
  bad_stuff_count = 0
  
  for box in unstored_boxes:
      box_adjacent = get_adjacent(box[0], box[1])
      
      for square in box_adjacent:
        if square in state.obstacles:
          bad_stuff_count += 1
          
        if square in state.boxes:
          bad_stuff_count += 1
  
      if(bad_stuff_count >= 2): 
        return True
      
      bad_stuff_count = 0
  
  return False

# checks if on the edge but theres no storage along the edge
# NOTE: this logic may actually be hella fucked?????? but i dont think so 
def edge_deadlock(state, box, edges):
  on_hor_edge = hor_lock = box[0] in edges[0]  # check if its on an edge
  on_vert_edge = vert_lock = box[1] in edges[1]
  
  if on_hor_edge or on_vert_edge: # if a box is on an edge
    for storage in state.storage: 
      if box != storage:
        if on_hor_edge and storage[0] == box[0]: 
          hor_lock = False
        if on_vert_edge and storage[1] == box[1]: 
          vert_lock = False
          
    if(hor_lock or vert_lock): # if one is true, then a lock exists
      return True
    
  return False
  
def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
  #IMPLEMENT
  # '''admissible sokoban puzzle heuristic: manhattan distance'''
  # '''INPUT: a sokoban state'''
  # '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  #We want an admissible heuristic, which is an optimistic heuristic.
  #It must never overestimate the cost to get from the current state to the goal.
  #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
  #When calculating distances, assume there are no obstacles on the grid.
  #You should implement this heuristic function exactly, even if it is tempting to improve it.
  #Your function should return a numeric value; this is the estimate of the distance to the goal.
  # print("running heur_manhattan_distance")

  total_dist = 0
  man_dist = math.inf
    
  for box in state.boxes:
    if box not in state.storage:
      for storage in state.storage:
        curr_dist = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
        man_dist = min(man_dist, curr_dist)
  
    if(man_dist != math.inf):
      total_dist += man_dist
      
    man_dist = math.inf
  
  return total_dist

def heur_manhattan_distance_altered(state, unstored_boxes):
  total_dist = 0
  man_dist = math.inf
    
  for box in unstored_boxes:
    for storage in state.storage:
      curr_dist = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
      man_dist = min(man_dist, curr_dist)
  
    if(man_dist != math.inf):
      total_dist += man_dist
      
    man_dist = math.inf
  
  return total_dist

def heur_robots_to_boxes(state, unstored_boxes):
  total_dist = 0
  man_dist = math.inf
  
  selected_box = (0,0)
  
  for robot in state.robots:
    if unstored_boxes: # check if list is not empty
      for box in unstored_boxes:
        curr_dist = abs(robot[0] - box[0]) + abs(robot[1] - box[1])  
        if(curr_dist < man_dist):
          man_dist = curr_dist
          selected_box = box
    
      if(man_dist != math.inf):
        total_dist += man_dist
        unstored_boxes.remove(selected_box)
        
      man_dist = math.inf
      
  return total_dist
    
#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def heur_alternate(state):
#  Of 2 initial problems, 13 were solved in less than 8 seconds by this solver.
#  Problems that remain unsolved in the set are Problems: [5, 9, 13, 15, 16, 17, 19]

  # IMPLEMENT
  '''a better heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # heur_manhattan_distance has flaws.
  # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
  # Your function should return a numeric value for the estimate of the distance to the goal.
  # print("heur alternate")
  
  global prev_info
  
  try: 
    prev_info
  except NameError: 
    prev_info = None
  
  if prev_info is None:                    prev_info = [state.boxes, math.inf]
  elif (prev_info[0] == state.boxes):      return prev_info[1]
  else:                                    prev_info[0] = state.boxes
  
  unstored_boxes = []
  for box in state.boxes:
    if box not in state.storage:
      unstored_boxes.append(box)

  # right off the bat, if this results in an impossible to solve state, stop
  if(deadlock_detector(state, unstored_boxes)):
    prev_info[1] = math.inf
    return math.inf
  
  # now gonna look at two things: 1) man dist and 2) dist of robots to boxes
  prev_info[1] = heur_manhattan_distance_altered(state, unstored_boxes) + heur_robots_to_boxes(state, unstored_boxes)
  return prev_info[1]

def heur_alternate_hash(state):
  global hash_table
  hash_key = ""
  
  try: 
    hash_table
  except NameError: 
    hash_table = None
  
  if hash_table is None:                   hash_table = {'-9': 0}
  elif (hash_key in hash_table):           return hash_table[hash_key]
  
  unstored_boxes = []
  for box in state.boxes:
    hash_key = hash_key + str(box[0]) + str(box[1])
    if box not in state.storage:
      unstored_boxes.append(box)
  
  hash_key = str(int(hash_key) % 4000067)
  
  # right off the bat, if this results in an impossible to solve state, stop
  if(deadlock_detector(state, unstored_boxes)):
    hash_table[hash_key] = math.inf
    return math.inf
  
  # now gonna look at two things: 1) man dist and 2) dist of robots to boxes
  # hash_table[hash_key] = heur_manhattan_distance_altered(state, unstored_boxes) + heur_robots_to_boxes(state, unstored_boxes)
  hash_table[hash_key] = heur_manhattan_distance_altered(state, unstored_boxes)
  return hash_table[hash_key]

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
    #IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
  #IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  se = SearchEngine(strategy = 'custom', cc_level = 'default')
  wrapped_fval_function = (lambda sN : fval_function(sN, weight))
  se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
  
  start_time = os.times()[0]
  elapsed_time = 0
  cost_bound = math.inf
  
  # find the first path 
  path = final_path = se.search(timebound=timebound, costbound=None) 
  
  # no path found yeet 
  if path == False:
    return False 
  else:
    cost_bound = path.gval
    
  while elapsed_time < timebound:
    path = se.search(timebound=(timebound - elapsed_time), costbound=(cost_bound, math.inf, math.inf))
    
    if path != False and path.gval < cost_bound:
      cost_bound, final_path = path.gval, path
          
    elapsed_time += os.times()[0] - start_time # update elapsed time
  
  # print('cost: {}'.format(cost_bound))
  return final_path



def anytime_gbfs(initial_state, heur_fn, timebound = 10):
  #IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  
  start_time = os.times()[0]; cost_bound = math.inf
  se = SearchEngine(strategy = 'best_first', cc_level = 'default')
  se.init_search(initial_state, sokoban_goal_state, heur_alternate)
  path = final_path = se.search(timebound=timebound, costbound=None) # find the first path  
  elapsed_time = 0
  
  # no path found yeet 
  if path == False:
    return False 
  
  cost_bound = path.gval
  
  while elapsed_time < timebound: # NOTE: ceil or not????????
    path = se.search(timebound=(timebound - elapsed_time), costbound=(cost_bound, math.inf, math.inf))
    
    if path != False and path.gval < cost_bound:
      cost_bound, final_path = path.gval, path
      
    elapsed_time += os.times()[0] - start_time # update elapsed time
    
  # print('cost: {}'.format(cost_bound))
  return final_path