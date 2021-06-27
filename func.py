import time
import DataStruct
import random

DEBUG = False

cafeteria_line1 = DataStruct.Line()
cafeteria_line2 = DataStruct.Line()

n_chair = 100
n_using_chair = int()
n_wait = int()
n_out = int()
n_side_dish = 7

lst_wait = list()
lst_wait_temp = list()
lst_getfood = list()
lst_available_chair = list(range(0, n_chair))
lst_buffer = list()
lst_friend_num = list()
lst_eating_students = list()
lst_available_chair_history = list()
lst_total_time = list()
lst_no_seat = list()

dict_chair = dict()

serving_speed = 5  # 10 people per minute
t_serving = n_side_dish * 5 / serving_speed / 60  # 50/60 min require
average_eating_speed = 15  # 15 min require for average
sigma_eating_speed = 5

average_friend_number = 4
sigma_friend_number = 0.5

n_simulate = 100
n_group_size_threshold = 5
n_scheduling_unit = 10  # when SJF, schedule for n_scheduling_unit and than n_scheduling_unit and ...


def delay(t):  # unit = minute
    time.sleep(t * 60 * 10 ** (-3))


# def change_status(index, is_using):
#     button = list_seat_graphic[index]
#     if is_using is True:
#         button["bg"] = "red"
#     else:
#         button["bg"] = "blue"


def get_continuous_seat():
    """
    :return: length, starting index
    """
    l = 0
    max_l = 0
    starting_index = 0
    for i in range(len(lst_available_chair) - 1):
        if lst_available_chair[i] == lst_available_chair[i+1]:
            l += 1
        else:
            max_l = max_l if max_l > l else l
            if max_l == l:
                starting_index = i - l + 1
    return l, starting_index


def eating_alone(student, lock):
    if DEBUG: print("========== eating_alone() IN ==========")

    if len(lst_available_chair) > 0:  # one seat i can eat
        lock.acquire()  # for avoiding crash
        site = random.choice(lst_available_chair)  # choose one seat
        dict_chair[site] = student  # add to using list
        lst_available_chair.remove(site)  # delete site while using

        # change_status(site, True)
        # print(f"available seat : {lst_available_chair}")
        lock.release()

        if DEBUG: print("========== eating_alone(): eating start 1==========")
        delay(student.get_eating_time())  # eating

        lock.acquire()
        lst_available_chair.append(site)  # release site while using

        # change_status(site, False)
        lock.release()
    else:
        # wait for 5 sec
        delay(5 / 60)
        student.add_time(5/60)  # add waiting time to total time
        # try again
        if len(lst_available_chair) > 0:
            lock.acquire()
            site = random.choice(lst_available_chair)
            dict_chair[site] = student  # add to using list
            lst_available_chair.remove(site)  # delete site while using

            # change_status(site, True)
            # print(f"available seat : {lst_available_chair}")
            lock.release()

            if DEBUG: print("========== eating_alone(): eating start 2==========")
            delay(student.get_eating_time())  # eating

            lock.acquire()
            lst_available_chair.append(site)  # release site while using

            del dict_chair[site]
            # change_status(site, False)
            lock.release()
        else:
            print("=============== No site error ===============")
            lst_no_seat.append(student)

    lock.acquire()
    lst_total_time.append(student.total_time)
    lock.release()


def students_in_cafeteria(student, lock):
    delay(student.total_time)
    n_friend = student.n_friend()
    if n_friend == 0:  # no friend
        eating_alone(student, lock)  # eat alone

    else:  # friend exist
        lst_eating_time = list()

        if student.is_leader():  # first student who in friend group
            continuous_seat_len, start_index = get_continuous_seat()  # get continuous seat
            if student.n_friend() + 1 <= continuous_seat_len:  # if friends can seat at once

                lock.acquire()
                my_site = lst_available_chair[start_index]  # set my seat to first place of continuous empty seat
                dict_chair[my_site] = student  # add to using chair
                lst_available_chair.remove(my_site)  # remove from available seat

                # change_status(my_site, True)  # change color of using seat
                # print(f"available seat : {lst_available_chair}")

                friends = student.return_friend()  # get friend list
                for i in range(student.n_friend()):
                    site = lst_available_chair[i + start_index + 1]  # get sequence of seat
                    lst_available_chair.remove(site)  # remove from available seat

                    dict_chair[site] = friends[i]  # add to using chair
                    # change_status(site, True)  # change color of using seat
                    friends[i].set_seatnum(site)  # save seat num
                    # print(f"available seat : {lst_available_chair}")
                    lst_eating_time.append(friends[i].eating_time())
                lock.release()

                max_eating_time = max(lst_eating_time)  # get max eating time
                student.set_eating_time(max_eating_time)  # set my eating time to maximum eating time
                student.set_status("eating")
                for friend in friends:
                    friend.set_eating_time(max_eating_time)  # re-set eating time
                    friend.set_status("eating")  # eat together

                delay(student.eating_time())  # eating

                lock.acquire()
                lst_available_chair.append(my_site)

                del dict_chair[my_site]
                lock.release()

            else:  # no seat for eating together
                eating_alone(student, lock)

        else:  # not a leader
            if student.status == "eating":
                delay(student.eating_time())  # eat

                lock.acquire()
                lst_available_chair.append(student.get_seatnum())

                del dict_chair[student.get_seatnum()]
                lock.release()
            else:
                delay(5/60)  # wait 5 sec for finding where my friends are eating
                student.add_time(5/60)  # add 5s to total time
                if student.status == "eating":
                    delay(student.eating_time())  # eat

                    lock.acquire()
                    lst_available_chair.append(student.get_seatnum())

                    del dict_chair[student.get_seatnum()]
                    lock.release()
                else:
                    eating_alone(student, lock)

    lst_wait.remove(student)  # delete student from lst_waiting


def recording():
    """record number of available chair"""
    if DEBUG: print("recording start")
    while len(lst_wait) > 0:
        delay(1/60)  # sampling rate: 1 Hz
        lst_available_chair_history.append(len(lst_available_chair))
        # print(f"available seat : {lst_available_chair}")
    if DEBUG: print("recording end")


def reset():
    lst_wait.clear()
    lst_wait_temp.clear()
    lst_getfood.clear()
    lst_buffer.clear()
    lst_friend_num.clear()
    lst_eating_students.clear()
    lst_available_chair_history.clear()
    lst_total_time.clear()
    lst_no_seat.clear()
    dict_chair.clear()
    cafeteria_line1.clear()
    cafeteria_line2.clear()
