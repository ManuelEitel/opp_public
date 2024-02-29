class OperatorAndAdminRights:
    def __init__(self):

        """
        Operator has a lot of rights. All the rights the Operator has, the Admin has them, too. \n
            modes: Possible UI Modes \n
                viewingMode: Can't interact with the cells from the table \n
                deleteMode: Can select rows to erase said rows \n
                reworkOrderMode: Can select rows to rework them \n
                distributeTasksMode: Can select rows/cells to open up the task bar \n
        """

        self.modes = {"viewingMode": True,
                      "deleteMode": False,
                      "reworkOrderMode": False,
                      "distributeTasksMode": False,
                      "distributeWorkflowMode": False}

        self.current_mode = "viewingMode"

    def change_mode(self, mode: str):
        """
        The operator chooses to change the state self.current_mode into the mode with title mode \n
        If a state is chosen again, then you get back into the viewingMode
        """
        if not self.get_mode(mode):
            self.modes = {x: False for x in self.modes}
            self.modes[mode] = True
            self.current_mode = mode
            return True
        else:
            self.modes = {x: False for x in self.modes}
            self.modes["viewingMode"] = True
            self.current_mode = "viewingMode"
            return False

    def get_mode(self, mode: str) -> bool:
        current_mode = self.modes.__getitem__(mode)
        return current_mode

