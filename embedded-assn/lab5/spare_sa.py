def RMS(**kwargs):
    capacity = kwargs['capacity']
    period = kwargs['period']
    prio,_ = list(map(lambda x:list(x),list(zip(*list(sorted(list(zip(list(range(len(period))),period)),key=lambda x:x[1]))))))
    remaining = copy.deepcopy(capacity)
    process_que = []
    final_list = []
    timer = [0]
    for p in prio:
        process_que.append(p)
    run_loop = Lcm(*period)
    for _ in range(run_loop):
        t = timer[-1]
        if (process_que.__len__() == 0):
            t += 1
            timer.append(t)
            final_list.append('blank')
            newly_arrived = [] # value = process
            for p in prio:
                if (t % period[p] == 0):
                    newly_arrived.append(p)
            for np in newly_arrived:
                remaining[np] = capacity[np]
                process_que.append(np)
            continue
        if (len(process_que) ==0):
            break
        pro = process_que.pop(0) # pro is index for quepresent and all
        final_list.append(pro)
        flagg = 0
        while (remaining[pro] != 0):
            t += 1
            remaining[pro] -= 1
            newly_arrived = [] # value = process
            for p in prio:
                if (t % period[p] == 0):
                    newly_arrived.append(p)
            if (newly_arrived.__len__() == 0):
                continue
            else:
                timer.append(t)
                flagg = 1
                flag = 0
                for np in newly_arrived:
                    remaining[np] = capacity[np]
                    if (prio.index(np) < prio.index(pro)):
                        process_que.append(np)
                    else:
                        if not flag:
                            flag = 1
                            process_que.append(pro)
                        process_que.append(np)
                if not flag:
                    process_que.append(pro)
                break
                

        if not flagg:
            timer.append(t)

    timerr = []
    for i in range(1,len(timer)):
        timerr.append(f'{timer[i-1]}-{timer[i]}')
    return final_list, timerr


def EDF(**kwargs):
    capacity = kwargs['capacity']
    deadline = kwargs['deadline']
    period = kwargs['period']
    final_list = []
    timer = [0]
    run_loop = Lcm(*period)
    is_present = [True] * len(period)
    for i in range(run_loop):
        t = timer[-1]
        pro = deadline.index(min(deadline))
        # print(is_present)
        # print(pro)
        if (not is_present[pro]):
            if (not any([is_present[m] == True for m in range(len(period))])):
                t+=1
                for idx,per in enumerate(period):
                    if t%per == 0:
                        is_present[idx] = True
                timer.append(t)
                final_list.append('blank')
                continue;
            
            deadl = math.inf
            for mypro in range(len(period)):
                if (is_present[mypro] and deadline[mypro] < deadl):
                    pro = mypro
                    deadl = deadline[mypro]
        # print(pro)
        if deadline[pro] < t:
            print(f'{pro} cannot be scheduled at {t}')
        is_present[pro] = False
        cap = capacity[pro]
        for j in range(1,cap+1):
            t += 1
            # check if some new process arrives
            for idx,per in enumerate(period):
                if t % per == 0:
                    is_present[idx] = True
        final_list.append(pro)
        timer.append(t)

        update_deadline = [0] * len(period)
        update_deadline[pro] = period[pro]
        deadline = add_arr(deadline,update_deadline)

    timerr = []
    for i in range(1,len(timer)):
        timerr.append(f'{timer[i-1]}-{timer[i]}')
    return final_list, timerr