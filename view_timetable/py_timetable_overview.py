from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from control_timetable.dragdropwidget import DragDropWidget


class ViewTimetableMain(QMainWindow):
    def __init__(self, model, user):

        super().__init__()
        self.model = model
        self.user = user
        loadUi("view_timetable/ui_files_timetable/timetable_main.ui", self)
        self.setAcceptDrops(True)
        self._name()


        #ToDo: set window modal

        self.widget_list = [self.monday_widget, self.tuesday_widget, self.wednesday_widget, self.thursday_widget,
                            self.friday_widget]



    def _name(self):
        self.top_label.setText(f'Weekly Timetable for employee {self.user}')

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):

        """ Setup Data of drop position and the text from the dragged widget """
        drop_pos = event.pos()
        drop_info = event.mimeData().text()  # take data from event

        """ Remove the dragged widget """
        dragged_item = event.source()
        source_weekday_widget = dragged_item.parent()
        source_weekday_widget.vertical_layout.removeWidget(dragged_item)  # remove dragged widget

        """ 
        Setup two cases of the drop
            * Case dropped onto a red widget -> It's parent widget will be out of self.widget_list.
            * Case dropped onto a weekday widget. So the grey area between the red items -> It's parent widget will be
              the week_widget itself.
              
                 
        """
        drop_ended_at_this_widget = self.childAt(drop_pos)
        either_workday_or_week_widget = drop_ended_at_this_widget.parent()

        """ 
        Work on Case 1: Dropped onto red widget
            The red widgets y-axis starts from the top of the main window downwards and they start at 112
            Use the graphic file 'timetable_main_help_coordinates_graphic.png for better understanding
            If the case 1 -> the either_workday_or_week_widget will be in self.widget list.
                We iterate through it and for the one, where we hit, we do something.
        """
        for element in self.widget_list:
            if either_workday_or_week_widget == element:

                """ y_min is the value inside the red widget, where we have a hit; add 112! """
                y_min = drop_ended_at_this_widget.geometry().y() + 112
                delta_y = drop_ended_at_this_widget.geometry().height()
                y_max = y_min + 112 + delta_y

                """ General test, if the drop_pos() is inside our allowed borders  """
                if int(y_min) <= int(drop_pos.y()) <= int(y_max):

                    """ Case: Lower half of the red widget was position, at which we dropped """
                    if int(drop_pos.y()) <= (int(y_min) + int(drop_ended_at_this_widget.geometry().height()) / 2):

                        for index in range(element.vertical_layout.count()):
                            """ Count the elements in that layout and tell me what how many widget we found """
                            item = element.vertical_layout.itemAt(index)
                            if item.widget() is not None and item.widget().objectName() == drop_ended_at_this_widget:
                                widget_found = item.widget()
                                widget_index = index
                                break
                    """ Case: Upper half of the red widget was position, at which we dropped """
                    if int(drop_pos.y()) > (int(y_min) + int(drop_ended_at_this_widget.geometry().height()) / 2):

                        for index in range(element.vertical_layout.count()):
                            """ Count the elements in that layout and tell me what how many widget we found """
                            item = element.vertical_layout.itemAt(index)
                            if item.widget() is not None and item.widget().objectName() == drop_ended_at_this_widget:
                                widget_found = item.widget()
                                widget_index = index

                """ Create new DragDropWidget and put it in index position and then setLayout() """
                new_widget = DragDropWidget(drop_info)
                new_widget.setStyleSheet("border: 1px solid black; background-color: red;")
                corrected_index = element.vertical_layout.count() - index

                element.vertical_layout.insertWidget(corrected_index, new_widget)
                element.setLayout(element.vertical_layout)

                event.accept()

    def set_initial_date(self, current_week: list, current_week_index: int):
        self.label_week_date.setText(f'Week: {current_week_index}')

        self.label_monday.setText(f'Monday\n{current_week[0]}')
        self.label_tuesday.setText(f'Tuesday\n{current_week[1]}')
        self.label_wednesday.setText(f'Wednesday\n{current_week[2]}')
        self.label_thursday.setText(f'Thursday\n{current_week[3]}')
        self.label_friday.setText(f'Friday\n{current_week[4]}')
