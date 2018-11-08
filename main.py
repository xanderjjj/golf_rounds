
import random

### Set variables here... ###
people = 10
rounds = 5
#############################

group_max = 4
group_min = group_max - 1

print("groups: {} - {} people".format(group_min, group_max))
print("rounds: {}".format(rounds))

def sizes(size, min, max):
    # single group case
    if size <= max:
        return [size]

    s = size
    l = []

    # divisible group case
    if size % max >= min or size % max == 0:
        while s >= max:
            s = s - max
            l.append(max)
        if s > 0:
            l.append(s)
        return sorted(l)

    # normalised group case
    while s >= min:
        s = s - min
        l.append(min)
    if s >= min - 1:
        l.append(s)
        s = 0
    if s < min and s > 0:
        l[-1] = l[-1] + s
    if len([x for x in l if x == min]) - 1 >= l[-1]:
        r = l[-1]
        del l[-1]
        for i in range(0, r):
            l[i] = l[i] + 1
    return sorted(l)

def place_people(group_sizes):
    group_list = []
    person = 0
    for group_size in group_sizes:
        new_group = []
        for slot in range(0, group_size):
            person = person + 1
            new_group.append(person)
        group_list.append(new_group)
    return group_list

def get_repeats(roster):
    people = 0
    for group in roster[0]:
        people = people + len(group)
    repeats = dict()
    for person in range(1, people + 1):
        opponents = dict()
        for opponent in range(1, people + 1):
            if opponent != person:
                opponents[opponent] = 0
        repeats[person] = opponents

    for round in roster:
        for group in round:
            for player in group:
                for opponent in group:
                    if player != opponent:
                        repeats[player][opponent] = repeats[player][opponent] + 1

    return repeats

def get_max_repeats(repeat_list):
    max_repeats = 0
    for player_key, player_value in repeat_list.items():
        for opponent_key, opponent_value in player_value.items():
            if opponent_value > max_repeats:
                max_repeats = opponent_value
    return max_repeats

def get_min_repeats(repeat_list):
    min_repeats = rounds
    for player_key, player_value in repeat_list.items():
        for opponent_key, opponent_value in player_value.items():
            if opponent_value < min_repeats:
                min_repeats = opponent_value
    return min_repeats

def get_min_repeat_count(repeat_list, min_repeats):
    min_repeat_count = 0
    for player_key, player_value in repeat_list.items():
        for opponent_key, opponent_value in player_value.items():
            if opponent_value == min_repeats:
                min_repeat_count = min_repeat_count + 1
    return min_repeat_count

def shuffle(round):
    people = 0
    for group in round:
        people = people + len(group)
    available = []
    assigned = []
    translation = dict()
    for person in range(1, people + 1):
        available.append(person)
    for person in range(1, people + 1):
        assign_to = random.choice(available)
        assigned.append(assign_to)
        available.remove(assign_to)
        translation[person] = assign_to
    for group_index in range(0,len(round)):
        for group_slot in range(0, len(round[group_index])):
            round[group_index][group_slot] = translation[round[group_index][group_slot]]
    return round


best_min_repeat_count = rounds * people
best_roster = []
best_repeat_list = dict()
best_max_repeats = rounds
best_min_repeats = rounds
for game in range(0, 500000):

    group_sizes = list(sizes(people, group_min, group_max))
    roster = []
    for round in range(1, rounds + 1):
        round_list = place_people(group_sizes=group_sizes)
        round_list = shuffle(round=round_list)
        roster.append(round_list)
    # print("roster: {}".format(roster))
    repeat_list = get_repeats(roster=roster)
    max_repeats = get_max_repeats(repeat_list=repeat_list)
    min_repeats = get_min_repeats(repeat_list=repeat_list)
    min_repeat_count = get_min_repeat_count(repeat_list=repeat_list, min_repeats=min_repeats)
    if max_repeats <= best_max_repeats and min_repeat_count < best_min_repeat_count:
        best_min_repeat_count = min_repeat_count
        best_roster = roster
        best_repeat_list = repeat_list
        best_max_repeats = max_repeats
        best_min_repeats = min_repeats


# print("roster: {}".format(roster))
for round in best_roster:
    print("round: {}".format(round))
print("repeats: {}".format(best_repeat_list))
print("max repeats: {}".format(best_max_repeats))
print("min repeats: {}".format(best_min_repeats))
print("min repeat count: {}".format(best_min_repeat_count))

