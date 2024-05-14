import unittest
from users.user_tasks import ManageUserTasks


class TestFindTimeSlotToday(unittest.TestCase):

    longMessage = True

    def test_find_time_slot_not_today(self):
        test_list_0 = [(480, 490), (490, 500), (520, 620), (780, 880)]  # Semi randomized Tasklist
        test_list_1 = [(480, 490)]  # Task at 8 o'Clock, nowhere else. Task short
        test_list_2 = [(480, 720)]  # Task at 8 o'Clock until 12 o'Clock
        test_list_3 = [(780, 1020)]  # Task through whole afternoon.
        test_list_4 = [(480, 720), (780, 1020)]  # Day completely blocked by two tasks
        test_list_5 = [(480, 490), (490, 500), (520, 620), (620, 720), (780, 880), (880, 1020)]  # Twenty min slot
        test_list_6 = [(480, 490), (520, 620), (620, 720), (780, 880), (880, 1020)]  # thirty minute slot at (490, 520)
        test_list_7 = [(490, 520), (520, 620), (620, 720), (780, 880), (880, 1020)]  # ten minute slot at (480, 490)
        test_list_8 = [(480, 720), (780, 880)]  # slot after the last task

        test_lists = [test_list_0, test_list_1, test_list_2, test_list_3, test_list_4, test_list_5, test_list_6,
                      test_list_7, test_list_8]

        expected_results_for_time_slot_is_ten = [
            ["17.04.2024", 500, 510],  # result_0
            ["17.04.2024", 490, 500],  # result_1
            ["17.04.2024", 780, 790],  # result_2
            ["17.04.2024", 480, 490],  # result_3
            [],  # result_4
            ['17.04.2024', 500, 510],  # result_5
            ["17.04.2024", 490, 500],  # result_6
            ["17.04.2024", 480, 490],  # result_7,
            ["17.04.2024", 880, 890]  # result_8
        ]

        expected_results_for_time_slot_is_one_hundred = [
            ["17.04.2024", 620, 720],  # result_0
            ["17.04.2024", 490, 590],  # result_1
            ["17.04.2024", 780, 880],  # result_2
            ["17.04.2024", 480, 580],  # result_3
            [],  # result_4
            [],  # result_5
            [],  # result_6
            [],  # result_7,
            ["17.04.2024", 880, 980]  # result_8
        ]

        expected_results_for_time_slot_is_twenty = [
            ["17.04.2024", 500, 520],  # result_0
            ["17.04.2024", 490, 510],  # result_1
            ["17.04.2024", 780, 800],  # result_2
            ["17.04.2024", 480, 500],  # result_3
            [],  # result_4
            ["17.04.2024", 500, 520],  # result_5
            ["17.04.2024", 490, 510],  # result_6
            [],  # result_7,
            ["17.04.2024", 880, 900]  # result_8
        ]

        for i, (test_list, expected) in enumerate(zip(test_lists, expected_results_for_time_slot_is_one_hundred)):
            with self.subTest(i=i):
                #print(f'i_0={i}')
                result = find_time_slot_not_today(time_delta_list=test_list, time_slot=100, date="17.04.2024")
                self.assertEqual(first=result, second=expected, msg="nice")

        for i, (test_list, expected) in enumerate(zip(test_lists, expected_results_for_time_slot_is_ten)):
            with self.subTest(i=i):
                #print(f'i_1={i}')
                result = find_time_slot_not_today(time_delta_list=test_list, time_slot=10, date="17.04.2024")
                self.assertEqual(first=result, second=expected, msg="nice")

        for i, (test_list, expected) in enumerate(zip(test_lists, expected_results_for_time_slot_is_twenty)):
            with self.subTest(i=i):
                #print(f'i_2={i}')
                result = find_time_slot_not_today(time_delta_list=test_list, time_slot=20, date="17.04.2024")
                self.assertEqual(first=result, second=expected, msg="nice")

    def test_find_time_slot_today(self):
        test_list_0 = [(480, 490), (490, 500), (520, 620), (780, 880)]  # Semi randomized Tasklist
        test_list_1 = [(480, 490)]  # Task at 8 o'Clock, nowhere else. Task short
        test_list_2 = [(480, 720)]  # Task at 8 o'Clock until 12 o'Clock
        test_list_3 = [(780, 1020)]  # Task through whole afternoon.
        test_list_4 = [(480, 720), (780, 1020)]  # Day completely blocked by two tasks
        test_list_5 = [(480, 490), (490, 500), (520, 620), (620, 720), (780, 880), (880, 1020)]  # Day full regularly
        test_list_6 = [(480, 490), (520, 620), (620, 720), (780, 880), (880, 1020)]  # thirty minute slot at (490, 520)
        test_list_7 = [(490, 520), (520, 620), (620, 720), (780, 880), (880, 1020)]  # ten minute slot at (480, 490)
        test_list_8 = [(480, 720), (780, 880)]
        test_list_9 = [(480, 510), (510, 555)]

        test_lists = [test_list_0, test_list_1, test_list_2, test_list_3, test_list_4, test_list_5, test_list_6,
                      test_list_7, test_list_8, test_list_9]

        exp_res_ts_100_now_480 = [
            ["17.04.2024", 620, 720],  # result_0
            ["17.04.2024", 490, 590],  # result_1
            ["17.04.2024", 780, 880],  # result_2
            ["17.04.2024", 480, 580],  # result_3
            [],  # result_4
            [],  # result_5
            [],  # result_6
            [],  # result_7,
            ["17.04.2024", 880, 980]  # result_8
        ]
        exp_res_ts_100_now_300 = [
            ["17.04.2024", 620, 720],  # result_0
            ["17.04.2024", 490, 590],  # result_1
            ["17.04.2024", 780, 880],  # result_2
            ["17.04.2024", 480, 580],  # result_3
            [],  # result_4
            [],  # result_5
            [],  # result_6
            [],  # result_7,
            ["17.04.2024", 880, 980],  # result_8
            ["17.04.2024", 555, 655]
        ]

        for i, (test_list, expected) in enumerate(zip(test_lists, exp_res_ts_100_now_300)):

            with (self.subTest(i=i)):
                self.manage_user_tasks = ManageUserTasks.find_time_slot_today(time_delta_shorted=test_list,
                                                                              time_slot=100, date="17.04.2024",
                                                                              now_in_int=300)

                self.assertEqual(first=self.manage_user_tasks, second=expected, msg="nice")
        """
        for i, (test_list, expected) in enumerate(zip(test_lists, exp_res_ts_100_now_480)):
            with self.subTest(i=i):
                #print(f'j_1={i}')
                result = find_time_slot_today(time_delta_list=test_list, time_slot=100, date="17.04.2024",
                                              now_in_int=480)
                self.assertEqual(first=result, second=expected, msg="nice")
        """


if __name__ == '__main__':
    unittest.main()
