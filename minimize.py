# Function to check if two states belong to the same equivalence class
def equivalent_states(state1, state2, equivalence_classes):
    for eq_class in equivalence_classes:
        if state1 in eq_class and state2 in eq_class:
            return True
    return False


# Main function for minimizing the DFA
def minimize(automaton):
    # Remove unreachable states from the automaton
    remove_unreachable_states(automaton)

    # Remove epsilon transitions (if any)
    remove_epsilon_transitions(automaton)

    # Initialization of the DFA minimization algorithm
    states = automaton['states']
    alphabet = automaton['alphabet']
    transitions = automaton['transitions']
    final_states = automaton['final_states']

    # Initialize equivalence classes based on final and non-final states
    non_final_states = list(set(states) - set(final_states))
    equivalence_classes = [final_states, non_final_states]

    # Step 1: Partition states based on their final status
    changed = True
    while changed:
        changed = False
        new_equivalence_classes = []

        for eq_class in equivalence_classes:
            for symbol in alphabet:
                # Group states with equivalent transitions
                new_class = []
                for state in eq_class:
                    next_state = \
                    [transition[2] for transition in transitions if transition[0] == state and transition[1] == symbol][
                        0]
                    if not equivalent_states(next_state, eq_class[0], equivalence_classes):
                        new_class.append(state)

                if new_class:
                    new_equivalence_classes.append(new_class)
                    changed = True

        equivalence_classes = new_equivalence_classes

    # Step 2: Merge equivalent states
    new_states = []
    for eq_class in equivalence_classes:
        new_state = "_".join(sorted(eq_class))
        new_states.append(new_state)

    new_transitions = []
    for transition in transitions:
        from_state = "_".join(sorted([transition[0]]))
        to_state = "_".join(sorted([transition[2]]))
        new_transitions.append([from_state, transition[1], to_state])

    new_final_states = ["_".join(sorted(eq_class)) for eq_class in equivalence_classes if
                        any(state in final_states for state in eq_class)]
    new_initial_state = "_".join(sorted([automaton['initial_state']]))

    # Construct the minimized DFA
    minimized_automaton = {
        'alphabet': alphabet,
        'states': new_states,
        'initial_state': new_initial_state,
        'final_states': new_final_states,
        'transitions': new_transitions
    }

    return minimized_automaton
