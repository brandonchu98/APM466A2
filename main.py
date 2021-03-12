import itertools
import matplotlib.pyplot as plt

STRIKE = 50
FACTOR = 1.1
WEEKS = 52


def tree_generator():
    tree_dict = {'': None}
    for j in range(WEEKS):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], j + 1)]
        for k in range(len(combinations)):
            tree_dict[''.join(sorted(combinations[k]))] = None
    return tree_dict


def price_convert(node):
    num_u = node.count('u')
    num_d = node.count('d')
    return ((FACTOR ** num_u) / (FACTOR ** num_d)) * STRIKE


def final_period_pricing_up(pricing_tree):
    combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 52)]
    for i in range(len(combinations)):
        if (price_convert(combinations[i])) - STRIKE > 0:
            pricing_tree[''.join(sorted(combinations[i]))] = (price_convert(combinations[i])) - STRIKE
        else:
            pricing_tree[''.join(sorted(combinations[i]))] = 0
    return pricing_tree


def probability_up(node):
    return (price_convert(node) - price_convert(node + 'd')) / (price_convert(node + 'u') - price_convert(node + 'd'))


def get_one_up_swing():
    one_up_swing = final_period_pricing_up(tree_generator())
    for i in range(WEEKS):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            price = (one_up_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        one_up_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            one_up_swing[''.join(sorted(combinations[j]))] = price
    return one_up_swing


one_up = get_one_up_swing()


def get_two_up_swing():
    two_up_swing = final_period_pricing_up(tree_generator())

    for i in range(WEEKS):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            not_exercise = (two_up_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        two_up_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = price_convert(combinations[j]) - STRIKE + one_up[''.join(sorted(combinations[j]))]
            two_up_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)
    return two_up_swing


two_up = get_two_up_swing()


def get_three_up_swing():
    three_up_swing = final_period_pricing_up(tree_generator())

    five_one_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51)]
    for k in range(len(five_one_combinations)):
        three_up_swing[''.join(sorted(five_one_combinations[k]))] = two_up[''.join(sorted(five_one_combinations[k]))]

    for i in range(WEEKS - 1):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 50 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            not_exercise = (three_up_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        three_up_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = price_convert(combinations[j]) - STRIKE + two_up[''.join(sorted(combinations[j]))]
            three_up_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)
    return three_up_swing


three_up = get_three_up_swing()
optimal_nodes_up = []


def get_four_up_swing():
    four_up_swing = final_period_pricing_up(tree_generator())

    optimal_weeks = []
    optimal_underlying = []

    five_two_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 52)]
    for k in range(len(five_two_combinations)):
        if round(price_convert(five_two_combinations[k]), 9) >= round(STRIKE, 9):
            optimal_weeks.append(len(five_two_combinations[k]))
            optimal_underlying.append(price_convert(('u' * 25) + ('d' * 27)))
    five_one_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51)]
    for k in range(len(five_one_combinations)):
        four_up_swing[''.join(sorted(five_one_combinations[k]))] = three_up[''.join(sorted(five_one_combinations[k]))]
        prob_up = probability_up(five_one_combinations[k])
        prob_down = 1 - prob_up
        not_exercise = (four_up_swing[''.join(sorted(five_one_combinations[k] + 'u'))] * prob_up) + (four_up_swing[''.join(sorted(five_one_combinations[k] + 'd'))] * prob_down)
        exercise = price_convert(five_one_combinations[k]) - STRIKE + three_up[''.join(sorted(five_one_combinations[k]))]
        if round(exercise, 9) >= round(not_exercise, 9):
            optimal_weeks.append(len(five_one_combinations[k]))
            optimal_underlying.append(price_convert(('u' * 25) + ('d' * 26)))
    five_zero_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 50)]
    for k in range(len(five_zero_combinations)):
        four_up_swing[''.join(sorted(five_zero_combinations[k]))] = three_up[''.join(sorted(five_zero_combinations[k]))]
        prob_up = probability_up(five_zero_combinations[k])
        prob_down = 1 - prob_up
        not_exercise = (four_up_swing[''.join(sorted(five_zero_combinations[k] + 'u'))] * prob_up) + (
                    four_up_swing[''.join(sorted(five_zero_combinations[k] + 'd'))] * prob_down)
        exercise = price_convert(five_zero_combinations[k]) - STRIKE + three_up[
            ''.join(sorted(five_zero_combinations[k]))]
        if round(exercise, 9) >= round(not_exercise, 9):
            optimal_weeks.append(len(five_zero_combinations[k]))
            optimal_underlying.append(price_convert(five_zero_combinations[k]))
    five_zero_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 50)]

    for i in range(WEEKS - 2):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 49 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            not_exercise = (four_up_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        four_up_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = price_convert(combinations[j]) - STRIKE + three_up[''.join(sorted(combinations[j]))]
            four_up_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)
            if round(exercise, 9) >= round(not_exercise, 9):
                # print(round(exercise, 9) - round(not_exercise, 9))
                # print(len(combinations[j]))
                # print(combinations[j])
                optimal_weeks.append(len(combinations[j]))
                optimal_underlying.append(price_convert(combinations[j]))
    optimal_nodes_up.append(optimal_weeks)
    optimal_nodes_up.append(optimal_underlying)
    return four_up_swing


four_up = get_four_up_swing()


optimal_nodes_up_dict = {}
for x in range(len(optimal_nodes_up[0])):
    optimal_nodes_up_dict[optimal_nodes_up[0][x]] = optimal_nodes_up[1][x]
print(optimal_nodes_up_dict)


print(optimal_nodes_up)
plot1 = plt.figure(1)
plt.plot(list(optimal_nodes_up_dict.keys()), list(optimal_nodes_up_dict.values()))
plt.title('4-upswing Optimal Exercise Boundary')
plt.xlabel('Time (Weeks)')
plt.ylabel('Underlying Price')

print(one_up)
print(two_up)
print(three_up)
print(four_up)
print('f')

STRIKE_DOWN = 50000


def price_convert_down(node):
    num_u = node.count('u')
    num_d = node.count('d')
    return ((FACTOR ** num_u) / (FACTOR ** num_d)) * STRIKE_DOWN


def final_period_pricing_down(pricing_tree):
    combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 52)]
    for i in range(len(combinations)):
        if STRIKE_DOWN - (price_convert_down(combinations[i])) > 0:
            pricing_tree[''.join(sorted(combinations[i]))] = STRIKE_DOWN - (price_convert_down(combinations[i]))
        else:
            pricing_tree[''.join(sorted(combinations[i]))] = 0
    return pricing_tree


def get_one_down_swing():
    one_down_swing = final_period_pricing_down(tree_generator())
    for i in range(WEEKS):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            price = (one_down_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        one_down_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            # one_down_swing[''.join(sorted(combinations[j]))] = price

            not_exercise = (one_down_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        one_down_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = STRIKE_DOWN - price_convert_down(combinations[j])
            one_down_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)

            # if exercise > not_exercise:
            #     print(exercise - not_exercise)
            #     print(len(combinations[j]))
            #     print(combinations[j])

    return one_down_swing


one_down = get_one_down_swing()
print(one_down)


def get_two_down_swing():
    two_down_swing = final_period_pricing_down(tree_generator())

    x = 0

    for i in range(WEEKS):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            not_exercise = (two_down_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        two_down_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = STRIKE_DOWN - price_convert_down(combinations[j]) + one_down[''.join(sorted(combinations[j]))]
            two_down_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)
            # if exercise > not_exercise:
            #     x += 1
            #     print(exercise - not_exercise)
            #     print(len(combinations[j]))
            #     print(combinations[j])
    return two_down_swing


two_down = get_two_down_swing()
print(two_down)


def get_three_down_swing():
    three_down_swing = final_period_pricing_down(tree_generator())

    five_one_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51)]
    for k in range(len(five_one_combinations)):
        three_down_swing[''.join(sorted(five_one_combinations[k]))] = two_down[
            ''.join(sorted(five_one_combinations[k]))]

    for i in range(WEEKS - 1):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 50 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            not_exercise = (three_down_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        three_down_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = STRIKE_DOWN - price_convert_down(combinations[j]) + two_down[''.join(sorted(combinations[j]))]
            three_down_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)
            # if exercise > not_exercise:
            #     print(exercise - not_exercise)
            #     print(len(combinations[j]))
            #     print(combinations[j])
    return three_down_swing


three_down = get_three_down_swing()
print(get_three_down_swing())


optimal_nodes_down = []


def get_four_down_swing():
    four_down_swing = final_period_pricing_down(tree_generator())

    optimal_weeks = []
    optimal_underlying = []

    five_two_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 52)]
    for k in range(len(five_two_combinations)):
        if round(price_convert_down(five_two_combinations[k]), 9) <= round(STRIKE_DOWN, 9):
            optimal_weeks.append(len(five_two_combinations[k]))
            optimal_underlying.append(price_convert_down(('u' * 27) + ('d' * 25)))
    five_one_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 51)]
    for k in range(len(five_one_combinations)):
        four_down_swing[''.join(sorted(five_one_combinations[k]))] = three_down[''.join(sorted(five_one_combinations[k]))]
        prob_up = probability_up(five_one_combinations[k])
        prob_down = 1 - prob_up
        not_exercise = (four_down_swing[''.join(sorted(five_one_combinations[k] + 'u'))] * prob_up) + (
                four_down_swing[''.join(sorted(five_one_combinations[k] + 'd'))] * prob_down)
        exercise = STRIKE_DOWN - price_convert_down(five_one_combinations[k]) + three_down[''.join(sorted(five_one_combinations[k]))]
        if round(exercise, 9) >= round(not_exercise, 9):
            optimal_weeks.append(len(five_one_combinations[k]))
            optimal_underlying.append(price_convert_down(('u' * 26) + ('d' * 25)))
    five_zero_combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 50)]
    for k in range(len(five_zero_combinations)):
        four_down_swing[''.join(sorted(five_zero_combinations[k]))] = three_down[''.join(sorted(five_zero_combinations[k]))]
        prob_up = probability_up(five_zero_combinations[k])
        prob_down = 1 - prob_up
        not_exercise = (four_down_swing[''.join(sorted(five_zero_combinations[k] + 'u'))] * prob_up) + (
                four_down_swing[''.join(sorted(five_zero_combinations[k] + 'd'))] * prob_down)
        exercise = STRIKE_DOWN - price_convert_down(five_zero_combinations[k]) + three_down[
            ''.join(sorted(five_zero_combinations[k]))]
        if round(exercise, 9) >= round(not_exercise, 9):
            optimal_weeks.append(len(five_zero_combinations[k]))
            optimal_underlying.append(price_convert_down(five_zero_combinations[k]))

    for i in range(WEEKS - 2):
        combinations = [''.join(i) for i in itertools.combinations_with_replacement(['u', 'd'], 49 - i)]
        for j in range(len(combinations)):
            prob_up = probability_up(combinations[j])
            prob_down = 1 - prob_up
            not_exercise = (four_down_swing[''.join(sorted(combinations[j] + 'u'))] * prob_up) + (
                        four_down_swing[''.join(sorted(combinations[j] + 'd'))] * prob_down)
            exercise = STRIKE_DOWN - price_convert_down(combinations[j]) + three_down[''.join(sorted(combinations[j]))]
            four_down_swing[''.join(sorted(combinations[j]))] = max(not_exercise, exercise, 0)
            if round(exercise, 9) >= round(not_exercise, 9):
                # print(exercise - not_exercise)
                # print(len(combinations[j]))
                # print(combinations[j])
                optimal_weeks.append(len(combinations[j]))
                optimal_underlying.append(price_convert_down(combinations[j]))
    optimal_nodes_down.append(optimal_weeks)
    optimal_nodes_down.append(optimal_underlying)
    return four_down_swing


# optimal_nodes_up_dict = {}
# for x in range(len(optimal_nodes_up[0])):
#     optimal_nodes_up_dict[optimal_nodes_up[0][x]] = optimal_nodes_up[1][x]
# print(optimal_nodes_up_dict)
#
#
# print(optimal_nodes_up)
# plot1 = plt.figure(1)
# plt.plot(list(optimal_nodes_up_dict.keys()), list(optimal_nodes_up_dict.values()))


four_down = get_four_down_swing()
print(four_down)

optimal_nodes_down_dict = {}
for y in range(len(optimal_nodes_down[0]) - 1, 0, -1):
    optimal_nodes_down_dict[optimal_nodes_down[0][y]] = optimal_nodes_down[1][y]


print(optimal_nodes_down)
plot2 = plt.figure(2)
plt.plot(list(optimal_nodes_down_dict.keys()), list(optimal_nodes_down_dict.values()))
plt.title('4-downswing Optimal Exercise Boundary')
plt.xlabel('Time (Weeks)')
plt.ylabel('Underlying Price')
plt.show()
