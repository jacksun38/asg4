'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    #store the (switching time, proccess_id) pair
    schedule = []
    queue = []
    waiting = []

    count = 0

    current_time = 0
    waiting_time = 0
    ending_time = []

    curr_proc = (-1,-1,-1)
    prev_proc = (-1,-1,-1)

    quantum = 0
    pos = 0

    proc_count = 0

    # do an iterative approach to simulate actual RR
    while 1:

        # insert item into the end of the queue
        for process in process_list:
            if process.arrive_time == current_time:
                # admit it into the queue
                print("\t\tprocess id: %d arrive_time: %d burst %d" %(process.id, process.arrive_time, process.burst_time))
                
                # tuple(process id, process arrive_time, process burst time, quantum consumed, waiting time, last ending time)
                queue.append([process.id, process.arrive_time, process.burst_time, 0, 0, process.arrive_time])
        
        # break into two parts
        # Part 1: settles the scheduling
        # Part 2: do the work

        # Part 1. decide who to gives the quantum to next    

        if len(queue) > 0:  # we have task waiting for scheduler
            print("[%d] scheduler is working" % current_time)

            # check if current quantum expired for the current process
            if quantum >= time_quantum or queue[pos][3] == queue[pos][2]: # quantum expired or task done

                if(queue[pos][3] == queue[pos][2]):
                    waiting_time = waiting_time + queue[pos][4]
                    print("len", len(queue))
                    queue.remove(queue[pos])
                    count = count + 1
                    print("len", len(queue))
                    pos = pos - 1
                else:
                    queue[pos][5] = current_time # update the ending time
                    

                    print("---> quantum expired for", queue[pos])
                    print("---> queue ", queue)

                if len(queue) > 1:
                    pos = (pos + 1) % len(queue) # update the pos to the next item in queue
                    
                else:
                    pos = 0
                print("    pos updated =>", pos)

                
                quantum = 0



                
        else:
            quantum = time_quantum


        # Part 2. do the work
        if len(queue) > 0:
            if quantum < time_quantum:
                
                if quantum == 0: # we just start, calcuate the waiting time
                    queue[pos][4] = queue[pos][4] + current_time - queue[pos][5]
                    schedule.append((current_time, queue[pos][0]))

                quantum = quantum + 1
                queue[pos][3] = queue[pos][3] + 1

                print("---> doing work on [%d], arrive_time: %d burst: %d workdone=%d waiting_time: %d" % (queue[pos][0], queue[pos][1], queue[pos][2], queue[pos][3], queue[pos][4]))
        else:
            print("[%d] scheduler is idle" % current_time)


        current_time = current_time + 1    
        
        if count >= len(process_list):
            break
        
  
    print(schedule)

    print("average waiting time: %f" % (waiting_time / 4))
    return (schedule, waiting_time / float(len(process_list)))

def SRTF_scheduling(process_list):
    schedule = []
    current_time = 0
    waiting_time = []
    queue = []
    dowork = 0
    count = 0

    while 1:
        # insert item into the end of the queue
        for process in process_list:
            if process.arrive_time == current_time:
                
                # admit it into the queue
                print("\t\tprocess id: %d arrive_time: %d burst %d" %(process.id, process.arrive_time, process.burst_time))
                
                queue.append((process.id, process.arrive_time, process.burst_time))
                
        if dowork == 0:
            # search for the shortest queue
            sjf = (-1, -1, 99999)

            if len(queue) > 0:
                for item in queue:
                    print("item [%d] arr: %d burst: %d" %(item[0], item[1], item[2]))
                
                    if(item[2] < sjf[2]):
                        sjf = item

                queue.remove(sjf)

                print("--> [%d] Working on %d with time=%d" % (current_time, sjf[0], sjf[2]))
                schedule.append((current_time, sjf[0]))
                count = count + 1

                waiting_time.append(current_time - sjf[1])
                dowork = sjf[2]
            else:
                print("--> [%d] idling", current_time)

        if dowork > 0:
            dowork = dowork - 1;
            print("--> [%d] Working on %d with time=%d" % (current_time, sjf[0], sjf[2]))
        

        current_time = current_time + 1

        if count == len(process_list):
            break

    total = 0.0

    for wt in waiting_time:
        total = total + wt

    print("average waiting time: %f" % (total / float(len(process_list))))
        
    print(schedule)
    return (schedule, (total / float(len(process_list))))

def SJF_scheduling(process_list, alpha):
    schedule = []
    current_time = 0
    waiting_time = 0
    queue = []
    dowork = 0
    pValue = {}
    pActual = {}

    current_proc = -1
    completed = 0

    #  Using α = 0.5, initial guess = 5 for all processes

    while 1:
        # insert item into the end of the queue
        for process in process_list:
            if process.arrive_time == current_time:
                procID = process.id
                # admit it into the queue
                
                
                # as the process arrive, calculate the predicted burst time
                # use the formula 'pValue = alpha * pActual + (1-alpha) * prevPvalue'
                if procID not in pValue: # we have seen this process id before
                    print(" \t--------- have not seen [%d] before" % procID)
                    pValue[procID] = 5  # set initial pValue to 5
                    pActual[procID] = 0 # have not seen, set it to 0 first

                print("\t\tprocess id: %d arrive_time: %d burst %d pvalue:=%f" %(process.id, process.arrive_time, process.burst_time, pValue[procID]))
                queue.append((process.id, process.arrive_time, process.burst_time, pValue[procID]))
                

        if dowork == 0:

            if current_proc > -1:
                # we have finished running
                # update the prediction for the next burst
                pValue[current_proc] = alpha * pActual[current_proc] + ( 1 - alpha) * pValue[current_proc] 
                print("-- t=[%d] Proc {%d} has completed. updating pvalue to %f" % (current_time,current_proc, pValue[current_proc]))
                completed = completed + 1

            # choose the next process
            if len(queue) > 0: # we have process in queue
                
                lowest_pred_val = (-1, -1, -1, 99999)

                # calculate the predicted value and choose the task with the lowest
                for item in queue:
                    procID = item[0]
                    print("-- t=[%d] Proc [%d] in queue" % (current_time,procID))
                    
                    if item[3] < lowest_pred_val[3]:
                        lowest_pred_val = item
                
                print("-- t=[%d] Selecting task: " % current_time, lowest_pred_val)

                schedule.append((current_time, lowest_pred_val[0]))
                
                current_proc = lowest_pred_val[0]
                dowork = lowest_pred_val[2]
                waiting_time = waiting_time + (current_time - lowest_pred_val[1])

                queue.remove(lowest_pred_val)
            else:
                current_proc = -1
                dowork = 0

        if dowork > 0:
            dowork = dowork - 1
            pActual[current_proc] = pActual[current_proc] + 1

            print("\t ---> working on [%d]" % current_proc)
        


        if(completed >= len(process_list)):
            break

        current_time = current_time + 1

    print(schedule)

    avg_wt = waiting_time / float(len(process_list))
    print("average waiting time %f" % (waiting_time / float(len(process_list))) )
    return (schedule,avg_wt)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result

def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)

    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
        
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

    print(FCFS_avg_waiting_time,RR_avg_waiting_time,SRTF_avg_waiting_time,SJF_avg_waiting_time)
if __name__ == '__main__':
    main(sys.argv[1:])