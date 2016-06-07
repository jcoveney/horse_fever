import copy
import random

track_length = 12

movement_cards=[
  [2,3,2,2,3,2],
  [2,2,2,2,1,0],
  [2,2,2,2,3,3],
  [2,4,2,2,0,2],
  [2,2,3,2,3,2],
  [2,2,2,2,1,1],
  [3,2,2,2,2,1],
  [2,2,3,2,2,3],
  [3,2,2,3,2,2],
  [3,3,2,2,2,2],
  [2,3,2,2,3,2],
  [2,3,2,2,2,3],
  [4,2,2,2,2,0],
  [4,3,2,2,2,2],
  [2,2,3,3,2,2],
  [3,2,3,2,2,2],
  [2,2,2,3,2,3],
  [3,3,2,2,2,2],
  [2,2,2,3,3,2],
  [2,2,3,1,2,2],
  [3,2,2,2,3,2],
  [3,2,2,2,2,3],
  [2,3,3,2,2,2],
]

def randomize_movement_deck():
  movement = copy.deepcopy(movement_cards)
  random.shuffle(movement)
  return movement

# this will update in place
def move_horses(is_start, horse_positions, movement, stop_if_first, move_if_last, start_move_fixed, start_move_plus):
  # In the case that a horse_position is None, meaning that horse has already placed, we don't want to incorporate
  # it's position
  present_horses = filter(lambda x: x != None, horse_positions)
  tail = min(present_horses)
  head = max(present_horses)

  for i in range(0, 6):
    if horse_positions[i] != None:
      if is_start and start_move_fixed[i] != None:
        horse_positions[i] = start_move_fixed[i]
      elif not is_start and i == stop_if_first and horse_positions[i] == head:
        pass
      elif not is_start and i == move_if_last and horse_positions[i] == tail:
        horse_positions[i] += 4
      else:
        horse_positions[i] += movement[i]

      # This means that it can stack with the start_move_fixed
      if is_start and start_move_plus[i] != None:
        horse_positions[i] += start_move_plus[i]

def sprint_dice(horse_positions, sprint_modifier):
  s = set()
  s.add(random.randint(0, 5))
  s.add(random.randint(0, 5))
  for p in s:
    if horse_positions[p] != None:
      horse_positions[p] += 1
      horse_positions[p] += sprint_modifier[p]

def determine_winners(horse_positions, finish_line_plus):
  new_winners = []

  for i in range(0, 6):
    pos = horse_positions[i]
    if pos != None and pos >= track_length:
      if finish_line_plus[i] != None:
        pos += finish_line_plus[i]
      new_winners.append((pos, i))

  # we want to sort position descending, but the horse index (ie odds) ascending
  return map(lambda x: x[1], sorted(new_winners, key=lambda x: (-x[0], x[1])))

def run_race(sprint_modifier, stop_if_first, move_if_last, start_move_fixed, start_move_plus, finish_line_plus):
  movement_deck = randomize_movement_deck()
  # every index corresponds to odds... we do not deal with multiple horses
  # with the same odds
  horse_positions = [0,0,0,0,0,0]

  # note that we want the WHOLE list...why? because we also want to report
  # the probability of moving up or down in odds
  winners = []

  is_start = True
  for movement in movement_deck:
    if len(winners) >= 6:
      return winners
    move_horses(is_start, horse_positions, movement, stop_if_first, move_if_last, start_move_fixed, start_move_plus)
    sprint_dice(horse_positions, sprint_modifier)

    new_winners = determine_winners(horse_positions, finish_line_plus)
    winners.extend(new_winners)
    for win in new_winners:
      horse_positions[win] = None
    is_start = False
  return winners

def simulate(iterations=100000,
             sprint_modifier=[0,0,0,0,0,0],
             stop_if_first=None,
             move_if_last=None,
             start_move_fixed=[None, None, None, None, None, None],
             start_move_plus=[None, None, None, None, None, None],
             finish_line_plus=[None, None, None, None, None, None]):
  wins = [0,0,0,0,0,0]
  shows = [0,0,0,0,0,0]
  #move_up = [0,0,0,0,0,0]
  #move_down = [0,0,0,0,0,0]
  for _ in range(0, iterations):
    winners = run_race(sprint_modifier, stop_if_first, move_if_last, start_move_fixed, start_move_plus, finish_line_plus)
    wins[winners[0]] += 1
    for i in range(0, 3):
      shows[winners[i]] += 1
  def div(xs):
    return map(lambda x: float(x)/iterations, xs)
  return (div(wins), div(shows))

def simulate_mod_sprint(sprint_mod):
  wins = []
  shows = []
  for i in range(0, 6):
    mod = [0,0,0,0,0,0]
    mod[i] = sprint_mod
    w, s = simulate(sprint_modifier=mod)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def simulate_stop_if_first():
  wins = []
  shows = []
  for i in range(0, 6):
    w, s = simulate(stop_if_first=i)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def simulate_move_if_last():
  wins = []
  shows = []
  for i in range(0, 6):
    w, s = simulate(move_if_last=i)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def simulate_start_four():
  wins = []
  shows = []
  for i in range(0, 6):
    start = [None] * 6
    start[i] = 4
    w, s = simulate(start_move_fixed=start)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def simulate_start_plus_1():
  wins = []
  shows = []
  for i in range(0, 6):
    start = [None] * 6
    start[i] = 1
    w, s = simulate(start_move_plus=start)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def simulate_start_zero():
  wins = []
  shows = []
  for i in range(0, 6):
    start = [None] * 6
    start[i] = 0
    w, s = simulate(start_move_fixed=start)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def simulate_finish_line_plus(plus):
  wins = []
  shows = []
  for i in range(0, 6):
    add = [None] * 6
    add[i] = plus
    w, s = simulate(finish_line_plus=add)
    wins.append(w)
    shows.append(s)
  return (wins, shows)

def printit(wins_shows):
  wins, shows = wins_shows
  print("wins")
  for w in wins:
    print('\t'.join(map(str, w)))
  print("shows")
  for s in shows:
    print('\t'.join(map(str, s)))


"""
w, s = horse_fever.simulate()
print("simulation")
print("wins")
print('\t'.join(map(str, w)))
print("shows")
print('\t'.join(map(str, s)))

results = {}
results['sprint_plus_1'] = horse_fever.simulate_mod_sprint(1) # sprint +1, alternately, sprint 2
results['sprint_plus_2'] = horse_fever.simulate_mod_sprint(2) # sprint +2
results['move_if_last'] = horse_fever.simulate_move_if_last()
results['start_zero'] = horse_fever.simulate_start_zero()
results['start_four'] = horse_fever.simulate_start_four()
results['start_plus_1'] = horse_fever.simulate_start_plus_1()
results['stop_if_first'] = horse_fever.simulate_stop_if_first()
results['no_sprint'] = horse_fever.simulate_mod_sprint(-1) # this is a sprint 0 as well
results['finish_line_plus_3'] = horse_fever.simulate_finish_line_plus(3)

for name, res in results.iteritems():
  print(name)
  horse_fever.printit(res)
"""