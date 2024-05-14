def order_current_steps(all_non_deprecated_user_tasks: list) -> list:

    ### test ###
    if len(all_non_deprecated_user_tasks) == 1:
        return all_non_deprecated_user_tasks

    else:
        sorted_tasks = sorted(all_non_deprecated_user_tasks)
        grouped_tasks = {}
        for task in sorted_tasks:
            key = task[0]
            if key not in grouped_tasks:
                grouped_tasks[key] = []
            grouped_tasks[key].append(task)
        return_list = [sorted(group, key=lambda x: x[3]) for group in grouped_tasks.values()]

        return return_list

test_list = [('29.03.2024', "2", "2", 200, 20, 0),
             ('27.03.2024', "2", "3", 150, 40, 0),
             ('28.03.2024', "d", "d", 100, 34, 0),
             ('27.03.2024', 'Initial_Step', 'Test_Workflow_2', 480, 600, 0),
             ('29.03.2024', "d", "e", 150, 20, 0),
             ('28.03.2024', "d", "d", 120, 20, 0),
             ('27.03.2024', "a", "a", 300, 300, 0)]

result = order_current_steps(test_list)

