import helperfunctions as hc
import copy

def preprocess(data):
    workflows = []
    inputs = []

    workflows_ = True
    for line in data:
        if line == '':
            workflows_ = False
            continue
        if workflows_:
            workflows.append(line)
        else:
            inputs.append(line)
    return workflows, inputs

def preprocess_workflows(workflows):
    actual_workflows = {}
    for workflow in workflows:
        workflow = workflow.replace('}', '')
        workflow = workflow.split('{')
        workflow_name = workflow[0].strip()
        workflow_steps = workflow[1].split(',')
        for i in range(len(workflow_steps)):
            workflow_step = workflow_steps[i]
            if ':' in workflow_step:
                workflow_step = workflow_step.split(':')
                rule = workflow_step[0]
                new_flow = workflow_step[1]
                if '<' in rule:
                    rule = rule.split('<')
                    actual_rule = ['<', rule[0], int(rule[1])]
                else:
                    rule = rule.split('>')
                    actual_rule = ['>', rule[0], int(rule[1])]
                workflow_steps[i] = [actual_rule, new_flow]
            else:
                workflow_steps[i] = [workflow_step]
        actual_workflows[workflow_name] = workflow_steps
    return actual_workflows

def preprocess_inputs(inputs):
    actual_inputs = []
    for input in inputs:
        new_input = {}
        input = input.replace('{', '').replace('}', '')
        input = input.split(',')
        for inp in input:
            inp = inp.split('=')
            new_input[inp[0]] = int(inp[1])
        actual_inputs.append(new_input)
    return actual_inputs

def apply_workflows(workflows, inputs):
    accepted = []
    for input in inputs:
        current_workflow = workflows['in']
        current_rule_pos = 0
        while True:
            current_rule = current_workflow[current_rule_pos]
            if len(current_rule) == 1:
                if current_rule[0] == 'A':
                    accepted.append(input)
                    break
                elif current_rule[0] == 'R':
                    break
                # new workflow
                current_workflow = workflows[current_rule[0]]
                current_rule_pos = 0
                continue
            operation = current_rule[0][0]
            l = current_rule[0][1]
            number = current_rule[0][2]
            result = current_rule[1]

            if operation == '<':
                if input[l] < number:
                    if result == 'A':
                        accepted.append(input)
                        break
                    elif result == 'R':
                        break
                    # new workflow
                    current_workflow = workflows[result]
                    current_rule_pos = 0
                    continue
                current_rule_pos += 1
            elif operation == '>':
                if input[l] > number:
                    if result == 'A':
                        accepted.append(input)
                        break
                    elif result == 'R':
                        break
                    # new workflow
                    current_workflow = workflows[result]
                    current_rule_pos = 0
                    continue
                current_rule_pos += 1
            else:
                raise Exception('Unknown operation')
        # break
    return accepted


def first_task():
    data = hc.read_file_line('19_2023')
    workflows, inputs = preprocess(data)
    workflows = preprocess_workflows(workflows)
    inputs = preprocess_inputs(inputs)
    acc = apply_workflows(workflows, inputs)

    sum_ = 0
    for a in acc:
        for key in a:
            sum_ += a[key]
    print(sum_)

POSSIBLE_VALUES = ['x', 'm', 'a', 's']

def solve_second_task_rek(workflows, 
                          current_workflow, 
                          current_rule_pos, 
                          current_number_range):
    
    current_rule = workflows[current_workflow][current_rule_pos]
    if len(current_rule) == 1:
        if current_rule[0] == 'A':
            prod = 1
            for key in POSSIBLE_VALUES:
                prod *= current_number_range[key][1] - current_number_range[key][0] + 1
            return prod
        elif current_rule[0] == 'R':
            return 0
        # new workflow
        return solve_second_task_rek(workflows, current_rule[0], 0, current_number_range)
    
    operation = current_rule[0][0]
    l = current_rule[0][1]
    number = current_rule[0][2]
    result = current_rule[1]

    if operation == '<':
        start_range, end_range = current_number_range[l][0], current_number_range[l][1]
        # print(l, number, start_range, end_range)
        if start_range >= number:
            # next rule
            return solve_second_task_rek(workflows, current_workflow, current_rule_pos + 1, current_number_range)
        elif end_range < number:
            # apply rule
            if result == 'A':
                prod = 1
                for key in POSSIBLE_VALUES:
                    prod *= current_number_range[key][1] - current_number_range[key][0] + 1
                return prod
            elif result == 'R':
                return 0
            # new workflow
            return solve_second_task_rek(workflows, result, 0, current_number_range)
        else:
            # split range
            lower_number_range = copy.deepcopy(current_number_range)
            lower_number_range[l][1] = number - 1

            upper_number_range = copy.deepcopy(current_number_range)
            upper_number_range[l][0] = number

            # print("range: ", lower_number_range, upper_number_range)

            # next rule
            # get lower end:
            if result == 'A':
                prod = 1
                for key in POSSIBLE_VALUES:
                    prod *= lower_number_range[key][1] - lower_number_range[key][0] + 1
                # print(f'Accepted: {prod}')
                lower_end = prod
            elif result == 'R':
                lower_end = 0
            else:
                lower_end = solve_second_task_rek(workflows, result, 0, lower_number_range)
            # get upper end:
            
            upper_end = solve_second_task_rek(workflows, current_workflow, current_rule_pos + 1, upper_number_range)
            return lower_end + upper_end
    elif operation == '>':
        start_range, end_range = current_number_range[l][0], current_number_range[l][1]
        if end_range <= number:
            # next rule
            return solve_second_task_rek(workflows, current_workflow, current_rule_pos + 1, current_number_range)
        elif start_range > number:
            # apply rule
            if result == 'A':
                prod = 1
                for key in POSSIBLE_VALUES:
                    prod *= current_number_range[key][1] - current_number_range[key][0] + 1
                return prod
            elif result == 'R':
                return 0
            # new workflow
            return solve_second_task_rek(workflows, result, 0, current_number_range)
        else:
            upper_number_range = copy.deepcopy(current_number_range)
            upper_number_range[l][0] = number + 1
            # split range
            lower_number_range = copy.deepcopy(current_number_range)
            lower_number_range[l][1] = number
            # next rule
            # get lower end:
            if result == 'A':
                prod = 1
                for key in POSSIBLE_VALUES:
                    prod *= upper_number_range[key][1] - upper_number_range[key][0] + 1
                lower_end = prod
            elif result == 'R':
                lower_end = 0
            else:
                lower_end = solve_second_task_rek(workflows, result, 0, upper_number_range)
            # get upper end:
            
            upper_end = solve_second_task_rek(workflows, current_workflow, current_rule_pos + 1, lower_number_range)
            return lower_end + upper_end


def second_task():
    data = hc.read_file_line('19_2023')
    workflows, _ = preprocess(data)
    workflows = preprocess_workflows(workflows)

    number_range = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
    ret = solve_second_task_rek(workflows, 'in', 0, number_range)
    print(ret)

# first_task()
second_task()