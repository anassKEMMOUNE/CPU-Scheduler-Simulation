


class Process:
    def __init__(self, id: int, burst_time: int, priority: int, arr_time: int, waiting_time: int = 0, cpu_time_acquired: int = 0, turnaround_time: int = 0) -> None:

        self.id = id
        self.burst_time = burst_time
        self.priority = priority
        self.arrival_time = arr_time

        # waiting time is the time between submission to system and starting execution 
        self.waiting_time = waiting_time
        self.cpu_time_acquired = cpu_time_acquired
        self.turnaround_time = turnaround_time

    def __str__(self):
        return str(self.id) + ',' + str(self.burst_time) + ',' + str(self.priority) + ',' + str(self.arrival_time) + ',' + str(self.turnaround_time) + ',' + str(self.cpu_time_acquired) +',' + str(self.waiting_time)

    def display(self):
        return f"Process {self.id} with burst time {self.burst_time} and priority {self.priority} and arrival time {self.arrival_time} and waiting time {self.waiting_time} and turnaround time {self.turnaround_time}"

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        else:
            return self.id < other.id


print("Done!")


