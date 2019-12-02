import util
import copy

class DepthFirstSearch:
    def solve(self, problem, find_all_solutions=False):
        """
        NOTE find_all_solutions won't necessarily find all possible solutions since the
        visited set only checks the state, so transpositions (i.e. different action sequences that
        result in the same board state) will be skipped on subsequent runs
        """
        # actions and total_cost will be set if there is a path,
        # otherwise, they will still be None
        self.actions = None
        self.total_cost = None
        self.num_states_explored = 0 # for comparison against UCS

        start_state = problem.start_state()
        frontier = [([], start_state),]
        visited = set([])
        actions_tried = []

        while len(frontier) > 0:
            prev_actions, state = frontier.pop()
            actions_tried.append(prev_actions)
            visited.add(state)
            self.num_states_explored += 1
            if self.num_states_explored % 250 == 0:
                print("explored", self.num_states_explored, "states")

            # print("---")
            # print("state: (prev actions were: %s)" % (prev_actions, ))
            # print("    ", state.graph)
            # print("    ", state.node_colors)
            # print("    moves left: %d" % (state.moves_left,))
            if problem.is_terminal_state(state) == 1:
                print("solution found! ", prev_actions)
                print("num states explored: ", self.num_states_explored)
                problem.actions = self.actions
                problem.num_states_explored = self.num_states_explored
                # print("explored these actions:")
                # for action_tried in actions_tried:
                #     print(action_tried)

                if find_all_solutions: continue
                else: break
            if problem.is_terminal_state(state) == -1:
                continue
            for (action, next_state, cost) in problem.actions_and_costs(state):
                if (next_state not in visited and
                    problem.is_terminal_state(next_state) != -1):
                        actions = copy.deepcopy(prev_actions)
                        actions.append(action)
                        frontier.append((actions, next_state))

class UniformCostSearch:
    def solve(self, problem):
        # actions and total_cost will be set if there is a path,
        # otherwise, they will still be None
        self.actions = None
        self.total_cost = None
        self.num_states_explored = 0 # to evaluate heuristic effectiveness

        frontier = util.PriorityQueue()
        # for backtracking (extracting solution): map state -> action, previous state
        predecessor = {}
        visited = set([])

        start_state = problem.start_state()
        frontier.update(start_state, 0)
        previous_g_cost = None
        while not frontier.empty():
            state, g_cost = frontier.remove_min()

            # print("min cost state from frontier:")
            # prev_actions = []
            # this_state = state
            # while this_state != start_state:
            #     action, this_state = predecessor[this_state]
            #     prev_actions.insert(0, action)
            # print(prev_actions)
            # print("g_cost =", g_cost)

            visited.add(state)
            self.num_states_explored += 1
            if previous_g_cost != g_cost:
                previous_g_cost = g_cost
                print(f"new g cost: {previous_g_cost}")
            
            if self.num_states_explored % 250 == 0:
                print("explored", self.num_states_explored, "states")

            if problem.is_terminal_state(state) == 1:
                print("solution found!")
                self.total_cost = g_cost
                self.actions = []
                while state != start_state:
                    action, state = predecessor[state]
                    self.actions.insert(0, action)
                problem.actions = self.actions
                problem.num_states_explored = self.num_states_explored
                print("actions: ", self.actions)
                print("num states explored: ", self.num_states_explored)
                # print("explored these actions:")
                # for state in visited:
                #     prev_actions = []
                #     while state != start_state:
                #         action, state = predecessor[state]
                #         prev_actions.insert(0, action)
                #     print(prev_actions)
                break
            if problem.is_terminal_state(state) == -1:
                continue

            for (action, next_state, next_cost) in problem.actions_and_costs(state):
                if (next_state not in visited and
                    problem.is_terminal_state(next_state) != -1):
                        # If we've found a better path, update the predecessor
                        if frontier.update(next_state, g_cost + next_cost):
                            predecessor[next_state] = (action, state)
