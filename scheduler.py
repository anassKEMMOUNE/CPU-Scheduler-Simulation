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

    # First_come_First_Served
    def first_come_first_served(self, Processes: List[Process]):
        # Sort by arrival time and for equal arrival time sort by process id:
        Processes.sort(key=lambda x: (x.arrival_time, x.id))
        # Calculate waiting time for each process
        current_time = Processes[0].arrival_time
        order = []
        for process in Processes:
            order.append(process.id)
            if process.arrival_time > current_time:
                current_time = process.arrival_time
            process.waiting_time = current_time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            current_time += process.burst_time
        Processes.sort(key=lambda x: x.id)
        return Processes, current_time, order

    # shortest job first
    @staticmethod
    def shortest_job_first(self, Processes: List[Process]):

        # we will use a heap to store the processes with the highest priority at the top
        # and we will push processes in the heap as they arrive and pop the process with the highest priority

        heap = []
        heapq.heapify(heap)

        # Sort by arrival time
        Processes.sort(key=lambda x: x.arrival_time)

        order = []

        current_process_idx = 0
        current_time = Processes[0].arrival_time

        # add all processes that have arrived to the heap
        while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
            heapq.heappush(heap, (Processes[current_process_idx].burst_time, Processes[current_process_idx]))
            current_process_idx += 1

        # Now while the queue is not empty we will take the element with the highest priority and calculate the waiting time and current time after the process finishes
        # and then we will push all processes that have arrived to the heap and repeat the process

        while heap:
            # print('Trated process:', heap[0][1].id)
            order.append(heap[0][1].id)

            process = heapq.heappop(heap)
            process[1].waiting_time = current_time - process[1].arrival_time
            process[1].turnaround_time = process[1].waiting_time + process[1].burst_time
            current_time += process[1].burst_time

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

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time, order

    ## Priority Scheduling
    @staticmethod
    def priority_scheduling(self, Processes: List[Process]):

        # we will use a heap to store the processes with the highest priority at the top
        # and we will push processes in the heap as they arrive and pop the process with the highest priority

        heap = []
        heapq.heapify(heap)

        # Sort by arrival time
        Processes.sort(key=lambda x: x.arrival_time)

        order = []

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
            order.append(heap[0][1].id)

            process = heapq.heappop(heap)
            process[1].waiting_time = current_time - process[1].arrival_time
            process[1].turnaround_time = process[1].waiting_time + process[1].burst_time
            current_time += process[1].burst_time

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

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time, order

    @staticmethod
    # shortest job first
    def Shortest_Job_First_2(Processes: List[Process]):

        # we will use a heap to store the processes with the highest priority at the top
        # and we will push processes in the heap as they arrive and pop the process with the highest priority

        file = open("static/csv/execution.csv", 'w')
        file.write("id,start,end"+"\n")

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
        print("execution.csv updated")
        Processes.sort(key=lambda x: x.id)
        return Processes, current_time


    @staticmethod
    # First_come_First_Served
    def First_come_First_Served_2(Processes: List[Process]):

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

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time


    @staticmethod
    ## Priority Scheduling
    def Priority_2(Processes: List[Process]):

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

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time




    @staticmethod
    def get_available(self):
        return ['FCFS', 'SJF', 'Priority Scheduling']

    def run_processes(self, opt : str, processes: List[Process]):
        if opt == 'FCFS':
            return self.First_come_First_Served_2(processes)
        if opt == 'SJF':
            return self.Shortest_Job_First_2(processes)
        if opt == 'Priority Scheduling':
            return self.Priority_2(processes)


class InteractiveScheduler(Scheduler):
    def __init__(self) -> None:
        pass

    # Round robin Algorithm

    @staticmethod
    def round_robin(self, Processes: List[Process], quantum: int, context_switching_time: int):

        # Sort by arrival time
        Processes.sort(key=lambda x: x.arrival_time)

        current_time = Processes[0].arrival_time
        finished_processes = 0

        queue = deque()
        current_process_idx = 0

        while current_process_idx < len(Processes) and Processes[current_process_idx].arrival_time <= current_time:
            queue.append(Processes[current_process_idx])
            current_process_idx += 1

        while finished_processes < len(Processes):

            if queue:
                process = queue.popleft()

                if process.cpu_time_acquired == 0:
                    process.waiting_time = current_time - process.arrival_time

                if process.burst_time <= quantum:
                    process.cpu_time_acquired += process.burst_time
                    current_time += process.burst_time
                    process.burst_time = 0
                    process.turnaround_time = current_time - process.arrival_time
                    finished_processes += 1

                else:
                    process.cpu_time_acquired += quantum
                    current_time += quantum
                    process.burst_time -= quantum

                    while current_process_idx < len(Processes) and Processes[
                        current_process_idx].arrival_time <= current_time:
                        queue.append(Processes[current_process_idx])
                        current_process_idx += 1

                    queue.append(process)


            else:
                current_time = Processes[current_process_idx].arrival_time

                while current_process_idx < len(Processes) and Processes[
                    current_process_idx].arrival_time <= current_time:
                    queue.append(Processes[current_process_idx])
                    current_process_idx += 1

        Processes.sort(key=lambda x: x.id)
        return Processes, current_time

    from collections import deque

    @staticmethod
    def priority_round_robin(self, processes: List[Process], quantum: int, context_switching_time: int):
        processes.sort(key=lambda x: x.arrival_time)

        # the priority classes range from -20 to 19
        queue_list = [deque() for _ in range(40)]

        current_time = processes[0].arrival_time
        process_index = 0
        finished_processes = 0
        n = len(processes)

        while process_index < n and processes[process_index].arrival_time == current_time:
            queue_list[processes[process_index].priority + 20].append(processes[process_index])
            process_index += 1

        while finished_processes < n:

            progress = finished_processes / n
            bar_length = 30
            bar = '=' * int(progress * bar_length) + '>' + '-' * (bar_length - int(progress * bar_length))
            print(f"\rProgress: [{bar}] {progress * 100:.2f}%", end='', flush=True)

            found = False
            for i in range(40):
                if len(queue_list[i]) > 0:
                    found = True
                    process = queue_list[i].popleft()

                    # print("-----> Operating on process ", process.id, " with priority ", process.priority, " at time ", current_time)

                    if process.cpu_time_acquired == 0:
                        process.waiting_time = current_time - process.arrival_time

                    if process.burst_time - process.cpu_time_acquired <= quantum:
                        current_time += process.burst_time - process.cpu_time_acquired
                        process.cpu_time_acquired = process.burst_time
                        process.turnaround_time = current_time - process.arrival_time
                        finished_processes += 1
                        while process_index < n and processes[process_index].arrival_time <= current_time:
                            # print("Added process ", processes[process_index].id, " to queue ")
                            queue_list[processes[process_index].priority + 20].append(processes[process_index])
                            process_index += 1
                        current_time += context_switching_time


                    else:
                        current_time += quantum
                        process.cpu_time_acquired += quantum
                        while process_index < n and processes[process_index].arrival_time <= current_time:
                            # print("Added process ", processes[process_index].id, " to queue ")
                            queue_list[processes[process_index].priority + 20].append(processes[process_index])
                            process_index += 1
                        queue_list[i].append(process)
                        current_time += context_switching_time

                    # print("-----> Finished process ", process.id, " at time ", current_time)
                    break

            if not found:
                current_time = processes[process_index].arrival_time
                while process_index < n and processes[process_index].arrival_time == current_time:
                    queue_list[processes[process_index].priority + 20].append(processes[process_index])
                    process_index += 1
        # sort the processes based on their id
        processes.sort(key=lambda x: x.id)
        return processes, current_time

    def get_available(self):
        return [" Round-Robin", "Priority Round-Robin"]

    def run_processes(self, opt : str, processes: List[Process], quantum: int, context_switching_time: int):
        if opt == "Priority Round-Robin":
            return self.priority_round_robin(processes, quantum, context_switching_time)
        if opt == "Round-Robin":
            return self.priority_round_robin(processes, quantum, context_switching_time)
        else:
            return None



