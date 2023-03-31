class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.wait_time = 0
        self.response_time = None

    def __str__(self):
        return f'PID: {self.pid}, Arrival Time: {self.arrival_time}, Burst Time: {self.burst_time}'

def read_processes_from_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        for line in file:
            pid, arrival_time, burst_time = map(int, line.split())
            processes.append(Process(pid, arrival_time, burst_time))
    return processes

def sjf_preemptive(processes):
    remaining_processes = processes.copy()
    current_time = 0
    completed_processes = []
    response_times = []
    while remaining_processes:
        next_process = None
        for process in remaining_processes:
            if process.arrival_time <= current_time and (next_process is None or process.remaining_time < next_process.remaining_time):
                next_process = process

        if next_process is None:
            current_time += 1
        else:
            if next_process.response_time is None:
                next_process.response_time = current_time - next_process.arrival_time
                response_times.append(next_process.response_time)
            next_process.remaining_time -= 1
            current_time += 1
            if next_process.remaining_time == 0:
                next_process.end_time = current_time
                next_process.wait_time = next_process.end_time - next_process.arrival_time - next_process.burst_time
                completed_processes.append(next_process)
                remaining_processes.remove(next_process)

    tat_sum = 0
    wt_sum = 0
    rt_sum = 0
    rd_sum = 0
    for process in completed_processes:
        tat_sum += process.end_time - process.arrival_time
        wt_sum += process.wait_time
        rt_sum += process.response_time
        rd_sum += process.wait_time / process.burst_time
    n = len(completed_processes)
    avg_tat = tat_sum / n
    avg_wt = wt_sum / n
    avg_rt = rt_sum / n
    avg_rd = rd_sum / n
    return (avg_tat, avg_wt, avg_rt, avg_rd)

if __name__ == '__main__':
    processes = read_processes_from_file('lelo.txt')
    avg_tat, avg_wt, avg_rt, avg_rd = sjf_preemptive(processes)
    print(f'Average Turnaround Time: {avg_tat:.2f}')
    print(f'Average Waiting Time: {avg_wt:.2f}')
    print(f'Average Response Time: {avg_rt:.2f}')
    print(f'Average Relative delay: {avg_rd:.2f}')
