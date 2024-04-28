from scheduler import Scheduler,BatchScheduler,InteractiveScheduler
from process import Process
from typing import List
import pandas as pd
import random as rand


class System:

    def __init__(self, scheduler: Scheduler = None, processes: List[Process] = None, context_switching_time: float = 0, quantum: float = 1) -> None:

        self.processes = processes
        self.scheduler = scheduler
        self.context_switching = context_switching_time
        self.quantum = quantum 

    def get_processes(self) -> List[Process]:
        return self.processes
    
    def set_processes(self, processes: List = List[Process]) -> None:
        self.processes = processes
    
    def add_process(self,process: Process) -> None:
        self.get_processes().append(process)

    def schedule(self,algorithm) :
        if isinstance(self.scheduler,BatchScheduler) :
            self.scheduler.run_processes(algorithm,self.processes)
        elif isinstance(self.scheduler,InteractiveScheduler)  :
            self.scheduler.run_processes(algorithm,self.processes,self.quantum,self.context_switching)
        

    @staticmethod
    def generate_processes(file_directory: str, number_of_processes: int,  max_burst: int, min_burst: int, max_arrival_time: int) -> []:
        """Function to generate random processes"""
        file = open(file_directory, 'w')
        file.write("id,burst_time,priority,arrival_time,turnaround_time,cpu_time_acquired,waiting_time" + '\n')
        processes = []
        for i in range(number_of_processes):
            
            id = i+1
            priority = rand.randint(-20, 19)
            burst_time = rand.randint(min_burst, max_burst)
            arrival_time = rand.randint(0,max_arrival_time)
            
            process = Process(id, burst_time, priority, arrival_time)
            processes.append(process)
            file.write(str(process) + '\n')

        file.close()
        print("Generated " + str(number_of_processes) + " processes into " + str(file_directory))
        return processes

    @staticmethod
    def load_from_csv(file_directory: str) -> []:
        """Function to load processes from a CSV file."""
        processes = []
        df = pd.read_csv(file_directory)
        for _,row in df.iterrows() :
            process = Process(row["id"], row["burst_time"],row["priority"], row["arrival_time"], row["turnaround_time"] , row["cpu_time_acquired"], row["waiting_time"])
            processes.append(process)

        return processes

    @staticmethod 
    def save_processes_csv(file_directory: str, processes: List[Process]) -> None:
        """Function to save processes to a CSV file """
        file = open(file_directory, 'w')
        file.write("id,burst_time,priority,arrival_time,turnaround_time,cpu_time_acquired,waiting_time" + '\n')
        for process in processes : 
            file.write(str(process) + '\n')

        file.close()
        print("Saved processes")


    # def run_processes(self):



    
a = System()

pro = System.generate_processes('test.csv', 100, 10, 10, 10)


    