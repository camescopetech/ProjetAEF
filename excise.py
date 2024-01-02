def epsilon_closure(state, transitions):
    # Return all the state accessible from a given one, following only a given transition
    closure = set([state])
    stack = [state]

    while stack:
        current_state = stack.pop()
        # Going all over the transitions to find the states accessible by this epsilon transition
        for transition in transitions:
            if transition[0] == current_state and transition[1] == '':
                next_state = transition[2]
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

    return closure

def reachable_states(initial_state, transitions):
    # Return all states accessible from the initial state
    reachable = set([initial_state])
    stack = [initial_state]

    while stack:
        current_state = stack.pop()
 
        # Going over the transitions to find the accessible states
        for transition in transitions:
            if transition[0] == current_state:
                next_state = transition[1]
                if next_state not in reachable:
                    reachable.add(next_state)
                    stack.append(next_state)

    return reachable

def epsilon_closure_of_set(states, transitions):
    # Return the set of all states reachable from any state in the automaton
    # by following epsilon transitions
    closure = set()
    for state in states:
        closure.update(epsilon_closure(state, transitions))

    return closure

def remove_unreachable_states(automate):
    # Remove all inacessible state
    initial_state = automate['initial_state']
    transitions = automate['transitions']

    reachable = reachable_states(initial_state, transitions)
    new_transitions = [transition for transition in transitions if transition[0] in reachable and transition[1] in reachable]

    automate['states'] = list(reachable)
    automate['transitions'] = new_transitions

def remove_epsilon_transitions(automate):
    # Remove all epsilon transition
    transitions = automate['transitions']

    epsilon_transitions = [transition for transition in transitions if transition[1] == '']

    while epsilon_transitions:
        for epsilon_transition in epsilon_transitions:
            from_state = epsilon_transition[0]
            to_state = epsilon_transition[2]
            epsilon_closure_set = epsilon_closure_of_set([to_state], transitions)

            for state in epsilon_closure_set:
                new_transition = [from_state, epsilon_transition[1], state]
                if new_transition not in transitions:
                    transitions.append(new_transition)

            transitions.remove(epsilon_transition)

        epsilon_transitions = [transition for transition in transitions if transition[1] == '']

"""automate = {
    'alphabet': ['a', 'b'],
    'states': ['0', '1', '2', '3'],
    'initial_state': '0',
    'final_states': ['2', '3'],
    'transitions': [
        ['0', '1', 'b'],
        ['0', '3', 'a'],
        ['1', '1', 'a'],
        ['1', '2', 'b'],
        ['3', '3', 'a']
    ]
}

remove_unreachable_states(automate)
remove_epsilon_transitions(automate)

print("Automate émondé:")
print(automate)"""
