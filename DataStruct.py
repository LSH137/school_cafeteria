class Student:
    def __init__(self, eating_time):
        self.eating_time = float(eating_time)
        self.total_time = 0
        self.friend_list = list()
        self.leader = False
        self.head = None  # student who lined first in the friends
        self.line = None
        self.status = "waiting"
        self.seatnum = 0

    def set_header(self, first):
        if self.leader is False:
            self.head = first

    def add_time(self, t):
        self.total_time = self.total_time + float(t)

    def set_eating_time(self, t):
        self.eating_time = float(t)

    def add_friend(self, friends):
        for f in friends:
            self.friend_list.append(f)

    def n_friend(self):
        return len(self.friend_list)

    def return_friend(self):
        return self.friend_list

    def is_leader(self):  # most front student in friend list
        return self.leader

    def get_eating_time(self):
        return self.eating_time

    def set_status(self, status):
        self.status = status

    def set_seatnum(self, seatnum):
        self.seatnum = seatnum

    def get_seatnum(self):
        return self.seatnum


class Line:
    def __init__(self):
        self.students_in_line = list()

    def n_students(self):
        return len(self.students_in_line)

    def add_students(self, students):
        if isinstance(students, list):  # str(type(students)) == "<class 'list'>":
            self.students_in_line = self.students_in_line + students
        else:
            self.students_in_line.append(students)

    def return_students(self):
        return self.students_in_line

    def clear(self):
        self.students_in_line.clear()
