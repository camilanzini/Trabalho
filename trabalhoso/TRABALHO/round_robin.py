from TRABALHO.taskgen import Tasks
from time import sleep



def prio(tasks: Tasks, preemp: bool) -> True:
    
    tasks_waiting: list[dict[str:int]] = []

    has_task: bool = True
    new_arrived: bool = True
    last_task = -1
    highest_prio = 0

    time = 1
    while has_task:

        sleep(.1) 

        for task in tasks:
            if task.get('arrival') <= time and task not in tasks_waiting and task.get('timeleft') != 0:
                tasks_waiting.append(task)


        if preemp:
            highest_prio = 0
            for task_index in range(len(tasks_waiting)):
                if tasks_waiting[task_index].get('prio') > tasks_waiting[highest_prio].get('prio'):
                    highest_prio = task_index

        else:    
            for i in range(len(tasks_waiting)):
                for task_num in range(len(tasks_waiting) - i - 1):

                    if tasks_waiting[task_num].get('arrival') > tasks_waiting[task_num+1].get('arrival'):

                        temp = tasks_waiting[task_num]
                        tasks_waiting[task_num] = tasks_waiting[task_num+1]
                        tasks_waiting[task_num+1] = temp

            for n in range(len(tasks_waiting)):
                for i in range(len(tasks_waiting) - n - 1):

                    if tasks_waiting[i].get('arrival') == tasks_waiting[i+1].get('arrival') and tasks_waiting[i].get('prio') < tasks_waiting[i+1].get('prio'):

                        temp = tasks_waiting[i]
                        tasks_waiting[i] = tasks_waiting[i+1]
                        tasks_waiting[i+1] = temp

        if len(tasks_waiting) > 0:

            if new_arrived or last_task != tasks_waiting[highest_prio].get("num"):
                print('-------------------------')
                print(f'Task {tasks_waiting[highest_prio].get("num")} arrived: ')

                tasks_waiting[highest_prio]['waiting'] = time - tasks_waiting[highest_prio]['arrival'] - (tasks_waiting[highest_prio].get('runtime') - tasks_waiting[highest_prio].get('timeleft'))

                new_arrived = False

            if tasks_waiting[highest_prio].get('timeleft') != 0:

                print(f"    Time [ {time} ] -  Timeleft: {tasks_waiting[highest_prio].get('timeleft')}")
                tasks_waiting[highest_prio]['timeleft'] -= 1
                last_task = tasks_waiting[highest_prio].get('num')
                
                if tasks_waiting[highest_prio].get('timeleft') == 0:
                    new_arrived = True
                    del tasks_waiting[highest_prio] 
        
        else:
            print(f"    Time [ {time} ] - no task ")

        time += 1
        has_task = False

        for task in tasks:
            if task.get('timeleft') > 0:
                has_task = True


    tasks.show_waiting_time()
    return True


if __name__ == "__main__":
    prio(Tasks(), preemp = True) 
    