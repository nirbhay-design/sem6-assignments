import random
import time
import os
import copy
import math

def Lcm(*args):
    lcm = args[0]
    for i in range(1,len(args)):
        lcm = int((lcm * args[i])/math.gcd(lcm,args[i]))
    return lcm

# # print(Lcm(20,5,10))
# inp = {'capacity':[3,2,2],
#         'deadline':[7,4,8],
#         'period':[20,5,10]
#     }
# inp = {'capacity':[2,2,2],
#         'deadline':[3,4,8],
#         'period':[3,4,8]
#     }
inp = {'capacity':[1,2,3,4,4,5],
        'deadline':[4,6,8,10,12,14],
        'period':[4,6,8,10,12,14]
    }


# inp = {'capacity':[2,2,2,2],
#         'deadline':[5,6,7,8],
#         'period':[5,6,7,8]
#     }

def add_arr(a1,a2):
    assert len(a1) == len(a2), "length should be same for both the arrays"
    for i in range(len(a1)):
        a1[i] += a2[i]
    return a1

def Edf(**kwargs):
    capacity = kwargs['capacity']
    deadline = kwargs['deadline']
    period = kwargs['period']
    sum_ci_ti = sum([capacity[i]/period[i] for i in range(len(capacity))])
    # if (sum_ci_ti > 1):
    #     return [],[]
    final_list = []
    timer = []
    run_loop = Lcm(*period)
    # running_capacity = copy.deepcopy(capacity)
    running_capacity = [0] * len(capacity)
    is_present = [True] * len(period)
    cur_pro = -1
    for tim in range(run_loop):
        ## fist check what all process has been arrived at this time
        for idx,per in enumerate(period):
            if tim % per == 0:
                if running_capacity[idx] != 0:
                    print(f'cannot schedule {idx}')
                    return [],[]
                is_present[idx] = True
                running_capacity[idx] = capacity[idx]


        ## finding process with min deadline
        mind = math.inf;pro = -1
        for i,d in enumerate(deadline):
            if (d < mind and is_present[i]):
                mind = d
                pro = i;
        # print(pro,tim)
        ## if not any process left then no cpu is idle
        if (pro == -1):
            timer.append(tim)
            final_list.append('blank')
            continue
        # print(pro,deadline,running_capacity)

        cur_pro = pro
        running_capacity[pro] = running_capacity[pro] - 1
        final_list.append(pro)
        timer.append(tim)

        ## updated the deadline for the process
        if running_capacity[pro] == 0:
            update_deadline = [0] * len(period)
            update_deadline[pro] = period[pro]
            deadline = add_arr(deadline,update_deadline)
            is_present[pro] = False
        else:
            if (tim >= deadline[pro]):
                print(f'deadline exceed for {pro}')
                return [],[]
    
    return final_list, timer

def Rms(**kwargs):
    capacity = kwargs['capacity']
    period = kwargs['period']
    n_process = len(capacity)
    sum_ci_ti = sum([capacity[i]/period[i] for i in range(len(capacity))])
    un = n_process * (math.pow(2,(1/n_process))-1)
    # if (sum_ci_ti > un):
    #     return [],[]
    # index is priority for prio and value is process
    prio,_ = list(map(lambda x:list(x),list(zip(*list(sorted(list(zip(list(range(len(period))),period)),key=lambda x:x[1]))))))
    print(f"priority: {prio}")
    remaining = copy.deepcopy(capacity)
    final_list = []
    timer = []
    run_loop = Lcm(*period)
    is_present = [True] * len(period)
    running_capacity = [0] * len(period)
    # print(prio)
    for tim in range(run_loop):
        # check if new process arrived
        for idx,per in enumerate(period):
            if (tim % per == 0):
                if (running_capacity[idx] != 0):
                    print(f'{idx} cannot be scheduled')
                    return [],[]
                is_present[idx] = True
                running_capacity[idx] = capacity[idx]

        pro = -1
        for pri,idx in enumerate(prio):
            if (is_present[idx]):
                pro = idx
                break;
        
        if (pro == -1):
            timer.append(tim)
            final_list.append('blank')
            continue

        running_capacity[pro] -= 1
        final_list.append(pro)
        timer.append(tim)

        if running_capacity[pro] == 0:
            is_present[pro] = False;

    return final_list,timer

print('####################__EDF__###################')    
final_list,timer = Edf(capacity = inp['capacity'],deadline=inp['deadline'],period=inp['period'])
# print(list(zip(timer,final_list)))
if len(final_list) ==0:
    print('some of the process cannot be scheduled')
else:
    for i,value in enumerate(final_list):
        print(f'{timer[i]} -> {final_list[i]}')

print("####################__RMS__###################")
# Rms(capacity = inp['capacity'],period=inp['period'])
final_list, timer = Rms(capacity = inp['capacity'],period=inp['period'])
# print(list(zip(timer,final_list)))
if len(final_list) == 0:
    print("some of the process cannot be scheduled")
else:
    for i,value in enumerate(final_list):
        print(f'{timer[i]} -> {final_list[i]}')