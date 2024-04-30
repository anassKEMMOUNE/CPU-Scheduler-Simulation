import queue
from process import Process
from typing import List
from typing import List
import heapq
from collections import deque
import random as rand
import pandas as pd




class Scheduler:
    def __init__(self) -> None:
        pass


class BatchScheduler(Scheduler):
    def __init__(self) -> None:
        pass


    @staticmethod
    # shortest job first
    def SJF(Processes: List[Process]):

        """
            Shortest Job First (SJF) scheduling algorithm.

            Args:
                Processes (List[Process]): List of processes with attributes: id, arrival_time, burst_time, waiting_time, turnaround_time.

            Returns:
                Tuple[List[Process], int]: A tuple containing the sorted list of processes with updated attributes and the total execution time.

            Description:
                This function implements the Shortest Job First (SJF) scheduling algorithm to minimize the average waiting time.
                It sorts the processes based on their arrival time, then processes them based on their burst time.
                Processes are stored in a heap where the process with the shortest burst time has the highest priority.
                The function writes the execution details to a CSV file and updates waiting time and turnaround time for each process.
                Finally, it writes the waiting time and turnaround time of each process to another CSV file.
            """

        # we will use a heap to store the processes with the highest priority at the top
        # and we will push processes in the heap as they arrive and pop the process with the highest priority

        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end" + "\n")

        heap = []
        heapq.heapify(heap)

        # Sort by arrival time
        Processes.sort(key=lambda x: x.arrival_time)

        current_process_idx = 0
        current_time = Processes[0].arrival_time

        # add all processes that have arrived to the heap
        while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
            heapq.heappush(heap, (Processes[current_process_idx].burst_time, Processes[current_process_idx]))
            current_process_idx += 1

        # Now while the queue is not empty we will take the element with the highest priority and calculate the waiting time and current time after the process finishes
        # and then we will push all processes that have arrived to the heap and repeat the process

        while heap:

            process = heapq.heappop(heap)

            file.write(str(process[1].id) + ',' + str(current_time) + ',')

            process[1].waiting_time = current_time - process[1].arrival_time
            process[1].turnaround_time = process[1].waiting_time + process[1].burst_time
            current_time += process[1].burst_time

            file.write(str(current_time) + '\n')

            while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
                heapq.heappush(heap, (Processes[current_process_idx].burst_time, Processes[current_process_idx]))
                current_process_idx += 1

            # now the heap might be empty but there are still processes that have not arrived yet
            # we will update the current time to the arrival time of the next process

            if current_process_idx < len(Processes) and heap == []:
                current_time = Processes[current_process_idx].arrival_time

            # now add the process to the heap
            while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
                heapq.heappush(heap, (Processes[current_process_idx].burst_time, Processes[current_process_idx]))
                current_process_idx += 1

        file.close()

        # open a csv file and write to it the maxium waiting times, the waiting times and turnaround times of each process
        file = open("static/csv/SpecialFile.csv", 'w')

        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.turnaround_time) + ',')

        file.close()

        print("execution.csv updated")
        Processes.sort(key=lambda x: x.id)
        return Processes, current_time

    @staticmethod
    # First_come_First_Served
    def FCFS(Processes: List[Process]):

        """
            First Come, First Served (FCFS) scheduling algorithm.

            Args:
                Processes (List[Process]): List of processes with attributes: id, arrival_time, burst_time, waiting_time, turnaround_time.

            Returns:
                Tuple[List[Process], int]: A tuple containing the sorted list of processes with updated attributes and the total execution time.

            Description:
                This function implements the First Come, First Served (FCFS) scheduling algorithm.
                It sorts the processes based on their arrival time and processes them in the order of arrival.
                The function writes the execution details to a CSV file and updates waiting time and turnaround time for each process.
                Finally, it writes the waiting time and turnaround time of each process to another CSV file.
            """

        # write the output to a csv file
        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end" + "\n")

        Processes.sort(key=lambda x: (x.arrival_time, x.id))

        # Calculate waiting time for each process
        current_time = Processes[0].arrival_time

        for process in Processes:

            if process.arrival_time > current_time:
                current_time = process.arrival_time

            file.write(str(process.id) + ',' + str(current_time) + ',')

            process.waiting_time = current_time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            current_time += process.burst_time

            file.write(str(current_time) + '\n')

        file.close()

        file = open("static/csv/SpecialFile.csv", 'w')

        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.turnaround_time) + ',')

        file.close()

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time

    @staticmethod
    ## Priority Scheduling
    def Priority_Scheduling(Processes: List[Process]):

        """
            Priority Scheduling algorithm.

            Args:
                Processes (List[Process]): List of processes with attributes: id, arrival_time, burst_time, priority, waiting_time, turnaround_time.

            Returns:
                Tuple[List[Process], int]: A tuple containing the sorted list of processes with updated attributes and the total execution time.

            Description:
                This function implements the Priority Scheduling algorithm.
                It uses a heap to store processes with the highest priority at the top, pushing processes as they arrive and popping the process with the highest priority.
                Processes are sorted by arrival time and added to the heap.
                The function writes the execution details to a CSV file and updates waiting time and turnaround time for each process.
                Finally, it writes the waiting time and turnaround time of each process to another CSV file.
            """

        # we will use a heap to store the processes with the highest priority at the top
        # and we will push processes in the heap as they arrive and pop the process with the highest priority

        heap = []
        heapq.heapify(heap)

        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end" + "\n")

        # Sort by arrival time
        Processes.sort(key=lambda x: x.arrival_time)

        current_process_idx = 0
        current_time = Processes[0].arrival_time

        # add all processes that have arrived to the heap
        while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
            heapq.heappush(heap, (Processes[current_process_idx].priority, Processes[current_process_idx]))
            current_process_idx += 1

        # Now while the queue is not empty we will take the element with the highest priority and calculate the waiting time and current time after the process finishes
        # and then we will push all processes that have arrived to the heap and repeat the process

        while heap:
            # print('Trated process:', heap[0][1].id)

            process = heapq.heappop(heap)

            file.write(str(process[1].id) + ',' + str(current_time) + ',')
            process[1].waiting_time = current_time - process[1].arrival_time
            process[1].turnaround_time = process[1].waiting_time + process[1].burst_time
            current_time += process[1].burst_time

            file.write(str(current_time) + '\n')

            while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
                heapq.heappush(heap, (Processes[current_process_idx].priority, Processes[current_process_idx]))
                current_process_idx += 1

            # now the heap might be empty but there are still processes that have not arrived yet
            # we will update the current time to the arrival time of the next process

            if current_process_idx < len(Processes) and heap == []:
                current_time = Processes[current_process_idx].arrival_time

            # now add the process to the heap
            while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
                heapq.heappush(heap, (Processes[current_process_idx].priority, Processes[current_process_idx]))
                current_process_idx += 1

        file = open("static/csv/SpecialFile.csv", 'w')

        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.turnaround_time) + ',')

        file.close()

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time



    @staticmethod
    def get_available(self):
        return ['FCFS', 'SJF', 'Priority Scheduling']

    def run_processes(self, opt : str, processes: List[Process]):

        """
            Run processes based on the selected scheduling algorithm.

            Args:
                opt (str): Scheduling algorithm option: "FCFS", "SJF", "Priority Scheduling".
                processes (List[Process]): List of processes.

            Returns:
                Union[Tuple[List[Process], int], None]: A tuple containing the sorted list of processes with updated attributes and the total execution time, or None if the option is invalid.

            Description:
                This method selects and runs the specified scheduling algorithm based on the given option.
                It returns the updated list of processes and the total execution time if the option is valid.
                If the option is invalid, it returns None.
            """

        if opt == 'FCFS':
            return self.FCFS(processes)
        if opt == 'SJF':
            return self.SJF(processes)
        if opt == 'Priority Scheduling':
            return self.Priority_Scheduling(processes)


class InteractiveScheduler(Scheduler):
    def __init__(self) -> None:
        pass

    # Round robin Algorithm

    # max waiting
    # waiting time
    # turnaround time


    @staticmethod
    # nearly done!
    def round_robin_with_aging(processes: List[Process], quantum: int, context_switching_time: int) -> List[Process]:

        """
            Round Robin with Aging scheduling algorithm.

            Args:
                processes (List[Process]): List of processes with attributes: id, arrival_time, burst_time, priority, waiting_time, turnaround_time, age, cpu_time_acquired, last_running_time, max_waiting_time.
                quantum (int): Time quantum for the Round Robin algorithm.
                context_switching_time (int): Time taken for context switching between processes.

            Returns:
                Tuple[List[Process], int]: A tuple containing the sorted list of processes with updated attributes and the total execution time.

            Description:
                This function implements the Round Robin with Aging scheduling algorithm.
                It uses a queue to store processes and processes them based on a given time quantum.
                Processes are aged based on their priority.
                The function writes the execution details to a CSV file and updates waiting time, turnaround time, and other attributes for each process.
                Finally, it writes the waiting time, turnaround time, and maximum waiting time of each process to a CSV file.
            """

        # this time we will write to a csv file which process is being executed and at what time
        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end\n")

        processes.sort(key=lambda x: x.arrival_time)

        queue = []

        current_time = processes[0].arrival_time
        process_index = 0
        finished_processes = 0
        n = len(processes)

        prev = -1

        while process_index < n and processes[process_index].arrival_time == current_time:
            heapq.heappush(queue, (processes[process_index].age, processes[process_index]))
            process_index += 1

        while finished_processes < n:

            # dipslay a progression bar here and delete it ater each progress
            # ...

            progress = finished_processes / n
            bar_length = 30
            bar = '=' * int(progress * bar_length) + '>' + '-' * (bar_length - int(progress * bar_length))
            print(f"\rProgress: [{bar}] {progress * 100:.2f}%", end='', flush=True)

            if len(queue) == 0:
                current_time = processes[process_index].arrival_time
                while process_index < n and processes[process_index].arrival_time == current_time:
                    heapq.heappush(queue, (processes[process_index].age, processes[process_index]))
                    process_index += 1

            age, process = heapq.heappop(queue)
            # print("Operating on process ", process.id, " with age ", process.age, " at time ", current_time)
            if prev == -1:
                prev = process.id

            if context_switching_time != 0 and prev != process.id:
                file.write("Context_Switch," + str(current_time) + ',')
                current_time += context_switching_time
                file.write(str(current_time) + '\n')

            file.write(str(process.id) + ',' + str(current_time) + ',')

            if process.burst_time - process.cpu_time_acquired <= quantum:
                process.max_waiting_time = max(process.max_waiting_time, current_time - process.last_running_time)
                current_time += process.burst_time - process.cpu_time_acquired
                process.cpu_time_acquired = process.burst_time
                process.turnaround_time = current_time - process.arrival_time
                process.last_running_time = current_time

                process.total_waiting_time = process.turnaround_time - process.burst_time
                finished_processes += 1
                file.write(str(current_time) + '\n')

                while process_index < n and processes[process_index].arrival_time <= current_time:
                    heapq.heappush(queue, (processes[process_index].age, processes[process_index]))
                    process_index += 1

            else:
                process.max_waiting_time = max(process.max_waiting_time, current_time - process.last_running_time)
                current_time += quantum
                process.cpu_time_acquired += quantum
                file.write(str(current_time) + '\n')
                process.last_running_time = current_time

                while process_index < n and processes[process_index].arrival_time <= current_time:
                    heapq.heappush(queue, (processes[process_index].age, processes[process_index]))
                    process_index += 1

                process.age += (process.priority + 21)
                heapq.heappush(queue, (process.age, process))

            prev = process.id

        file.close()

        # compute the waiting time for each process
        for process in processes:
            process.waiting_time = process.turnaround_time - process.burst_time

        # sort the processes based on their id
        processes.sort(key=lambda x: x.id)

        #  write into a csv file.
        file = open("SpecialFile.csv", 'w')

        for process in processes:
            file.write(str(process.max_waiting_time) + ',')
        file.write('\n')
        for process in processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in processes:
            file.write(str(process.turnaround_time) + ',')

        file.close()

        return processes, current_time
    @staticmethod
    # nearly done!
    def round_robin(Processes: List[Process], quantum: int, context_switching_time: int):

        """
            Round Robin scheduling algorithm.

            Args:
                Processes (List[Process]): List of processes with attributes: id, arrival_time, burst_time, waiting_time, turnaround_time, max_waiting_time, cpu_time_acquired, last_running_time.
                quantum (int): Time quantum for the Round Robin algorithm.
                context_switching_time (int): Time taken for context switching between processes.

            Returns:
                Tuple[List[Process], int]: A tuple containing the sorted list of processes with updated attributes and the total execution time.

            Description:
                This function implements the Round Robin scheduling algorithm.
                It uses a deque to store processes and processes them based on a given time quantum.
                The function writes the execution details to a CSV file and updates waiting time, turnaround time, and other attributes for each process.
                Finally, it writes the waiting time, turnaround time, and maximum waiting time of each process to a CSV file.
            """

        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end" + '\n')
        Processes.sort(key=lambda x: x.arrival_time)

        current_time = Processes[0].arrival_time
        finished_processes = 0

        queue = deque()

        # current_process_idx is the index of the next process that will arrive
        current_process_idx = 0

        while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
            queue.append(Processes[current_process_idx])
            current_process_idx += 1

        prev = -1

        while finished_processes < len(Processes):

            # first we do a context switch

            # we pick the first process in the queue and execute it for the quantum time
            # if the process finishes before the quantum time we will update the current time and the process

            if queue:
                process = queue.popleft()

                if prev == -1:
                    prev = process.id

                if context_switching_time != 0 and prev != process.id:
                    file.write("Context_Switch," + str(current_time) + ',')
                    current_time += context_switching_time
                    file.write(str(current_time) + '\n')

                file.write(str(process.id) + ',' + str(current_time) + ',')

                # print("runnnig process", process.id)
                if process.burst_time - process.cpu_time_acquired <= quantum:
                    process.max_waiting_time = max(process.max_waiting_time, current_time - process.last_running_time)

                    process.cpu_time_acquired = process.burst_time
                    current_time += process.burst_time - process.cpu_time_acquired

                    process.turnaround_time = current_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time

                    process.last_running_time = current_time
                    finished_processes += 1

                    while current_process_idx < len(Processes) and Processes[
                        current_process_idx].arrival_time <= current_time:
                        queue.append(Processes[current_process_idx])
                        current_process_idx += 1



                else:
                    process.max_waiting_time = max(process.max_waiting_time, current_time - process.last_running_time)

                    process.cpu_time_acquired += quantum
                    current_time += quantum
                    process.last_running_time = current_time

                    while current_process_idx < len(Processes) and Processes[
                        current_process_idx].arrival_time <= current_time:
                        queue.append(Processes[current_process_idx])
                        current_process_idx += 1

                    queue.append(process)

                prev = process.id
                file.write(str(current_time) + '\n')


            else:
                current_time = Processes[current_process_idx].arrival_time

                while current_process_idx < len(Processes) and Processes[
                    current_process_idx].arrival_time <= current_time:
                    queue.append(Processes[current_process_idx])
                    current_process_idx += 1

        # sort the processes based on their id
        Processes.sort(key=lambda x: x.id)

        #  write into a csv file.
        file = open("static/csv/SpecialFile.csv", 'w')

        for process in Processes:
            file.write(str(process.max_waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in Processes:
            file.write(str(process.turnaround_time) + ',')

        file.close()

        return Processes, current_time

    @staticmethod
    # nearly done!
    def priority_round_robin(processes: List[Process], quantum: int, context_switching_time: int) -> List[Process]:

        """
            Priority Round Robin scheduling algorithm.

            Args:
                processes (List[Process]): List of processes with attributes: id, arrival_time, burst_time, priority, waiting_time, turnaround_time, max_waiting_time, cpu_time_acquired, last_running_time.
                quantum (int): Time quantum for the Round Robin algorithm.
                context_switching_time (int): Time taken for context switching between processes.

            Returns:
                Tuple[List[Process], int]: A tuple containing the sorted list of processes with updated attributes and the total execution time.

            Description:
                This function implements the Priority Round Robin scheduling algorithm.
                It uses multiple queues to store processes based on their priority.
                Processes are processed in a round-robin manner within each priority queue.
                The function writes the execution details to a CSV file and updates waiting time, turnaround time, and other attributes for each process.
                Finally, it writes the waiting time, turnaround time, and maximum waiting time of each process to a CSV file.
            """

        # this time we will write to a csv file which process is being executed and at what time
        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end" + '\n')
        processes.sort(key=lambda x: x.arrival_time)

        # the priority classes range from -20 to 19
        queue_list = [deque() for _ in range(40)]

        current_time = processes[0].arrival_time
        process_index = 0
        finished_processes = 0
        n = len(processes)

        prev = -1

        while process_index < n and processes[process_index].arrival_time == current_time:
            queue_list[processes[process_index].priority + 20].append(processes[process_index])
            process_index += 1

        while finished_processes < n:

            # dipslay a progression bar here and delete it ater each progress
            # ...

            progress = finished_processes / n
            bar_length = 30
            bar = '=' * int(progress * bar_length) + '>' + '-' * (bar_length - int(progress * bar_length))
            print(f"\rProgress: [{bar}] {progress * 100:.2f}%", end='', flush=True)

            found = False
            for i in range(40):
                if len(queue_list[i]) > 0:
                    found = True
                    process = queue_list[i].popleft()

                    if prev == -1:
                        prev = process.id

                    if context_switching_time != 0 and prev != process.id:
                        file.write("Context_Switch," + str(current_time) + ',')
                        current_time += context_switching_time
                        file.write(str(current_time) + '\n')

                    file.write(str(process.id) + ',' + str(current_time) + ',')

                    # print("-----> Operating on process ", process.id, " with priority ", process.priority, " at time ", current_time)

                    if process.burst_time - process.cpu_time_acquired <= quantum:
                        process.max_waiting_time = max(process.max_waiting_time,
                                                       current_time - process.last_running_time)

                        current_time += process.burst_time - process.cpu_time_acquired
                        process.cpu_time_acquired = process.burst_time
                        process.turnaround_time = current_time - process.arrival_time

                        process.waiting_time = process.turnaround_time - process.burst_time
                        process.last_running_time = current_time

                        finished_processes += 1
                        file.write(str(current_time) + '\n')

                        while process_index < n and processes[process_index].arrival_time <= current_time:
                            # print("Added process ", processes[process_index].id, " to queue ")
                            queue_list[processes[process_index].priority + 20].append(processes[process_index])
                            process_index += 1



                    else:
                        process.max_waiting_time = max(process.max_waiting_time,
                                                       current_time - process.last_running_time)

                        current_time += quantum
                        process.cpu_time_acquired += quantum
                        file.write(str(current_time) + '\n')

                        process.last_running_time = current_time

                        while process_index < n and processes[process_index].arrival_time <= current_time:
                            # print("Added process ", processes[process_index].id, " to queue ")
                            queue_list[processes[process_index].priority + 20].append(processes[process_index])
                            process_index += 1
                        queue_list[i].append(process)

                    prev = process.id
                    # print("-----> Finished process ", process.id, " at time ", current_time)
                    break

            if not found:
                current_time = processes[process_index].arrival_time
                while process_index < n and processes[process_index].arrival_time == current_time:
                    queue_list[processes[process_index].priority + 20].append(processes[process_index])
                    process_index += 1

        file.close()

        # sort the processes based on their id
        processes.sort(key=lambda x: x.id)

        #  write into a csv file.
        file = open("static/csv/SpecialFile.csv", 'w')

        for process in processes:
            file.write(str(process.max_waiting_time) + ',')
        file.write('\n')
        for process in processes:
            file.write(str(process.waiting_time) + ',')
        file.write('\n')
        for process in processes:
            file.write(str(process.turnaround_time) + ',')
        file.write('\n')

        file.close()

        return processes, current_time

    def get_available(self):
        return [" Round-Robin", "Priority Round-Robin","Round-Robin with Aging"]

    def run_processes(self, opt: str, processes: List[Process], quantum: int, context_switching_time: int):

        """
            Run processes based on the selected scheduling algorithm.

            Args:
                opt (str): Scheduling algorithm option: "Priority Round-Robin", "Round-Robin", "Round-Robin with Aging".
                processes (List[Process]): List of processes.
                quantum (int): Time quantum for the Round Robin algorithms.
                context_switching_time (int): Time taken for context switching between processes.

            Returns:
                Union[Tuple[List[Process], int], None]: A tuple containing the sorted list of processes with updated attributes and the total execution time, or None if the option is invalid.

            Description:
                This method selects and runs the specified scheduling algorithm based on the given option.
                It returns the updated list of processes and the total execution time if the option is valid.
                If the option is invalid, it returns None.
            """

        if opt == "Priority Round-Robin":
            return self.priority_round_robin(processes, quantum, context_switching_time)
        if opt == "Round-Robin":
            return self.round_robin(processes, quantum, context_switching_time)
        if opt == "Round-Robin with Aging":
            return self.round_robin_with_aging(processes, quantum, context_switching_time)
        else:
            return None



