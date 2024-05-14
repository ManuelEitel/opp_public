import unittest
from model.model_operator import OperatorAndAdminRights
import regex as re


class TestCallControlSignUp(unittest.TestCase):
    """
    Does a bool come back, when the function has its input
    """

    def test_change_mode_bool_viewingMode(self):

        TrueFalse_Tester = OperatorAndAdminRights().change_mode("viewingMode")
        self.assertIsInstance(TrueFalse_Tester, bool)

    def test_change_mode_bool_deleteMode(self):

        TrueFalse_Tester = OperatorAndAdminRights().change_mode("deleteMode")
        self.assertIsInstance(TrueFalse_Tester, bool)

    def test_change_mode_bool_reworkOrderMode(self):

        TrueFalse_Tester = OperatorAndAdminRights().change_mode("reworkOrderMode")
        self.assertIsInstance(TrueFalse_Tester, bool)

    def test_change_mode_bool_distributeTasksMode(self):

        TrueFalse_Tester = OperatorAndAdminRights().change_mode("distributeTasksMode")
        self.assertIsInstance(TrueFalse_Tester, bool, msg="Nice")


class Test(unittest.TestCase):

    def order_current_steps(all_non_deprecated_user_tasks: list) -> list:
        sorted_tasks = sorted(all_non_deprecated_user_tasks)
        print(f'sorted_tasks = {sorted_tasks}')
        ### test ###
        if len(sorted_tasks) == 1:
            print(f'case: only one timeframe')
            return sorted_tasks

        sort_helper_list = []
        sort_list = []
        for i in range(len(sorted_tasks) - 1):

            if sorted_tasks[i][0] == sorted_tasks[i + 1][0]:  # same day events; same date
                sort_helper_list.append(sorted_tasks[i])

            if sorted_tasks[i][0] != sorted_tasks[i + 1][0]:
                sort_helper_list.append(sorted_tasks[i])
                sort_list.append(sort_helper_list)
                sort_helper_list = []

        return sort_list

    def test_order_dates_lists(self):
        test_list = [('27.03.2024', "2", "3", 150, 40, 0),
                     ('28.03.2024', "d", "d", 100, 34, 0),
                     ('27.03.2024', 'Initial_Step', 'Test_Workflow_2', 480, 600, 0),
                     ('29.03.2024', "d", "e", 150, 20, 0),
                     ('28.03.2024', "d", "d", 120, 20, 0),
                     ('27.03.2024', "a", "a", 300, 300, 0)]

        second =[[('27.03.2024', '2', '3', 150, 40, 0), ('27.03.2024', 'Initial_Step', 'Test_Workflow_2', 480, 600, 0),
                 ('27.03.2024', 'a', 'a', 300, 300, 0)], [('28.03.2024', 'd', 'd', 100, 34, 0),
                                                          ('28.03.2024', 'd', 'd', 120, 20, 0)]]

        TrueFalse_Tester = self.order_current_steps(test_list)
        self.assertEqual(first=TrueFalse_Tester, second=second, msg="Got the test")

    def string_progress_reader(self, test_strings: list):

        for element in test_strings:
            match = re.findall(r'\d*/', element)
            match = match[0][:-1]
            match2 = re.findall(r'/\d*', element)
            match2 = match2[0][1:]
            int_got = int(match)
            int_from = int(match2)

            if int_got <= int_from:
                pass
            else:
                return False

        return True

    def test_string_progress_reader(self):
        test_strings = ["0/4", "1/4", "2/4", "3/4", "123/1234", "20/20"]
        True_False_Tester = self.string_progress_reader(test_strings)
        self.assertTrue(True_False_Tester, msg="All good")


if __name__ == '__main__':
    unittest.main()
