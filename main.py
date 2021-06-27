import numpy as np
import DataStruct
import threading
import matplotlib.pyplot as plt
import func as f
import os
import scheduling as sch

lst_friend_num_history = list()
lst_meantime_history = list()
lst_mintime_history = list()
lst_maxtime_history = list()
grid = (2, 2)
schedule_algorithm = "FCFS"

if __name__ == '__main__':

    # get original condition
    n_wait = int(input("enter number of waiting students: "))
    if not os.path.exists(f"/home/lsh/Documents/informatics_project/{schedule_algorithm}"):
        os.makedirs(f"/home/lsh/Documents/informatics_project/{schedule_algorithm}")
    if not os.path.exists(f"/home/lsh/Documents/informatics_project/{schedule_algorithm}/{n_wait}"):
        os.makedirs(f"/home/lsh/Documents/informatics_project/{schedule_algorithm}/{n_wait}")

    for work in range(f.n_simulate):
        f.reset()
        # set size of friends
        f.lst_friend_num = f.sigma_friend_number * np.random.randn(n_wait // f.average_friend_number) + f.average_friend_number
        f.lst_friend_num = [int(i) for i in f.lst_friend_num if i > 0]  # number of friend is non-negative
        for n in f.lst_friend_num:
            lst_friend_num_history.append(n)  # friend num history

        # set eating time
        eating_speed = f.sigma_eating_speed * np.random.randn(n_wait) + f.average_eating_speed
        eating_speed = [abs(i) for i in eating_speed]  # eating speed is non-negative
        for i in range(n_wait):
            f.lst_wait_temp.append(DataStruct.Student(eating_speed[i]))

        # using cafeteria with friends
        index = 0
        for n in f.lst_friend_num:
            n = int(n)
            if n > 0:
                if f.DEBUG: print(f.lst_wait_temp)
                friends = f.lst_wait_temp[index:index + n]
                friends[0].leader = True
                for friend in friends:
                    friend.set_header(friends[0])
                for student in friends:
                    student.add_friend(friends)
                index = index + n

        sch.FCFS()  # scheduling
        # sch.SJF()
        # sch.LJF()

        # calculate time while waiting cafeteria_line1
        n_present_people = 0
        for student in f.cafeteria_line1.return_students():
            student.add_time((50 / 7) / 60 * n_present_people)
            n_present_people += 1

        # calculate time while waiting cafeteria_line2
        n_present_people = 0
        for student in f.cafeteria_line2.return_students():
            student.add_time((50 / 7) / 60 * n_present_people)
            n_present_people += 1

        # add time while get food
        for student in f.lst_wait:
            student.add_time(f.t_serving)

        # prepare for eating
        lock = threading.Lock()

        for student in f.lst_wait:
            eating_student = threading.Thread(target=f.students_in_cafeteria, args=(student, lock))
            eating_student.start()
            f.lst_eating_students.append(eating_student)

        record_thread = threading.Thread(target=f.recording)
        record_thread.start()
        f.lst_eating_students.append(record_thread)

        for student in f.lst_eating_students:
            student.join()

        print(f"========== {round((work + 1)/f.n_simulate * 100)} % end ==========")
        print(f"no seat: {len(f.lst_no_seat)}")
        plt.figure(num=work+1, clear=True)
        plt.figure(figsize=(8, 8))

        box = {'ec': (0.8, 0.8, 0.8), 'fc': (0.9, 0.9, 0.9)}
        ax1 = plt.subplot2grid(grid, (0, 0), rowspan=1, colspan=1)
        plt.title("number of available seat : time")
        plt.plot(f.lst_available_chair_history, "r-")
        plt.ylabel("number of available seat")
        plt.xlabel("time [sec]")
        plt.grid(True)
        plt.xticks([i * 300 for i in range(round(len(f.lst_available_chair_history) / 300))])
        if len(f.lst_no_seat) > 0:
            font_seat = {"size": 8}
            plt.text(1200, 10, f"no seat: {len(f.lst_no_seat)} people", fontdict=font_seat, bbox=box)
        # plt.savefig(f"/home/lsh/Documents/informatics_project/n={n_wait}_available_seat_graph.png", facecolor='#eeeeee')

        ax2 = plt.subplot2grid(grid, (0, 1), rowspan=1, colspan=1)
        plt.title("friend group size distribution")
        plt.hist(f.lst_friend_num, range=(0.5, 10.5))
        plt.xlabel("number of member")
        plt.ylabel("number of group")
        plt.grid(True)
        plt.xticks(list(range(0, 11)))
        # plt.savefig(f"/home/lsh/Documents/informatics_project/n={n_wait}_friend_group_hist.png", facecolor='#eeeeee')

        ax3 = plt.subplot2grid(grid, (1, 0), rowspan=1, colspan=2)
        plt.title("total time distribution")
        n, _, _ = plt.hist(f.lst_total_time, bins=50, histtype="bar", range=(0, 10))
        plt.xlabel("total time taken")
        plt.ylabel("number of students")
        plt.grid(True)
        plt.xticks([i / 2 for i in range(0, 21)])
        np_total_time = np.array(f.lst_total_time)
        mean_total_time = round(float(np.mean(np_total_time)), 2)
        min_total_time = round(float(np.min(np_total_time)), 2)
        max_total_time = round(float(np.max(np_total_time)), 2)
        lst_meantime_history.append(mean_total_time)
        lst_maxtime_history.append(max_total_time)
        lst_mintime_history.append(min_total_time)
        font = {"weight": "bold", "size": 12}
        plt.text(8, max(n) - 1,
                 f"mean: {mean_total_time} [min]\nmin: {min_total_time} [min]\nmax: {max_total_time} [min]",
                 fontdict=font, bbox=box)
        plt.subplots_adjust(left=0.11, bottom=0.11, right=0.90, top=0.90, wspace=0.3, hspace=0.3)
        plt.savefig(f"/home/lsh/Documents/informatics_project/{schedule_algorithm}/{n_wait}/n={n_wait}_test:{work}_group_size_threshold={f.n_group_size_threshold}_mean_group_size={f.average_friend_number}.png", facecolor='#eeeeee')

        plt.close('all')

    plt.figure(f.n_simulate + 1)
    plt.figure(figsize=(8, 8))
    plt.subplot2grid(grid, (0, 0), rowspan=1, colspan=1)
    plt.title("friend group size distribution")
    plt.hist(lst_friend_num_history, range=(0.5, 10.5))
    plt.xlabel("number of member")
    plt.ylabel("number of group")
    plt.grid(True)
    plt.xticks(list(range(0, 11)))

    plt.subplot2grid(grid, (0, 1), rowspan=1, colspan=1)
    plt.title("mean time taken")
    plt.hist(lst_meantime_history)
    plt.xlabel("mean time")
    plt.ylabel("number of people")
    plt.grid(True)

    plt.subplot2grid(grid, (1, 0), rowspan=1, colspan=1)
    plt.title("min time taken")
    plt.hist(lst_mintime_history)
    plt.xlabel("min time")
    plt.ylabel("number of people")
    plt.grid(True)

    plt.subplot2grid(grid, (1, 1), rowspan=1, colspan=1)
    plt.title("max time taken")
    plt.hist(lst_maxtime_history)
    plt.xlabel("max time")
    plt.ylabel("number of people")
    plt.grid(True)

    plt.subplots_adjust(left=0.11, bottom=0.11, right=0.90, top=0.90, wspace=0.3, hspace=0.3)

    plt.savefig(f"/home/lsh/Documents/informatics_project/n={n_wait}_sch={schedule_algorithm}_group_size_threshold={f.n_group_size_threshold}_mean_group_size={f.average_friend_number}.png", facecolor='#eeeeee')
    plt.show()
