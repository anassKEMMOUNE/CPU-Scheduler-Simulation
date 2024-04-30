from scheduler import Scheduler,BatchScheduler,InteractiveScheduler
from process import Process
from typing import List
import random as rand
import pandas as pd


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
        """
            Schedule processes using the specified algorithm.

            Parameters:
            - algorithm (str): The scheduling algorithm to use.

            Returns:
            - str: The scheduling result.

            Raises:
            - TypeError: If the scheduler is not an instance of BatchScheduler or InteractiveScheduler.

            Note:
            The method delegates the scheduling task to the appropriate scheduler based on the type of scheduler
            set for the current instance. If the scheduler is a BatchScheduler, it calls the 'run_processes' method
            of BatchScheduler with the specified algorithm and processes. If the scheduler is an InteractiveScheduler,
            it calls the 'run_processes' method of InteractiveScheduler with the specified algorithm, processes,
            quantum, and context switching time.
            """
        if isinstance(self.scheduler,BatchScheduler) :
            return self.scheduler.run_processes(algorithm,self.processes)
        elif isinstance(self.scheduler,InteractiveScheduler)  :
            return self.scheduler.run_processes(algorithm,self.processes,self.quantum,self.context_switching)
        

    @staticmethod
    def generate_processes(file_directory: str, number_of_processes: int,  max_burst: int, min_burst: int, max_arrival_time: int) -> []:
        """
            Function to generate random processes and write them to a file.

            Args:
                file_directory (str): File directory to write the generated processes.
                number_of_processes (int): Number of processes to generate.
                max_burst (int): Maximum burst time for the processes.
                min_burst (int): Minimum burst time for the processes.
                max_arrival_time (int): Maximum arrival time for the processes.

            Returns:
                List[Process]: List of generated processes.

            Description:
                This function generates random processes with specified attributes and writes them to a CSV file.
        """
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
        """
        Function to load processes from a CSV file.

        Args:
            file_directory (str): File directory to load processes from.

        Returns:
            List[Process]: List of loaded processes.

        Description:
            This function reads processes from a CSV file and creates Process objects from the data.
        """
        processes = []
        df = pd.read_csv(file_directory)
        for _,row in df.iterrows() :
            process = Process(row["id"], row["burst_time"],row["priority"], row["arrival_time"], row["turnaround_time"] , row["cpu_time_acquired"], row["waiting_time"])
            processes.append(process)

        return processes

    @staticmethod 
    def save_processes_csv(file_directory: str, processes: List[Process]) -> None:
        """
            Function to save processes to a CSV file.

            Args:
                file_directory (str): File directory to save processes.
                processes (List[Process]): List of processes to save.

            Description:
                This function writes processes to a CSV file.
            """
        file = open(file_directory, 'w')
        file.write("id,burst_time,priority,arrival_time,turnaround_time,cpu_time_acquired,waiting_time" + '\n')
        for process in processes : 
            file.write(str(process) + '\n')

        file.close()
        print("Saved processes")



    def system_to_csv(self,file_directory : str) :
        scheduler_name  = "batch" if isinstance(self.scheduler,BatchScheduler) else "interactive"
        file = open(file_directory,"w")
        file.write(scheduler_name+","+str(self.quantum)+","+str(self.context_switching))
        file.close()

    @staticmethod
    def load_system_txt(file_directory : str,processes = List[Process]) :
        """
            Function to load system configuration from a text file.

            Args:
                file_directory (str): File directory to load system configuration from.
                processes (List[Process]): List of processes.

            Returns:
                System: Loaded system configuration.

            Description:
                This function reads system configuration from a text file and creates a System object.
            """
        file = open(file_directory,"r")
        line = file.readlines()[0].split(",")
        sch = BatchScheduler() if line[0] == "batch" else InteractiveScheduler()
        syst = System(sch,processes,int(line[1]),int(line[2]))
        file.close()
        return syst
    





    



    