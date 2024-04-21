from TRABALHO.taskgen import Tasks
from time import sleep



def sjf(tasks: Tasks, preemp: bool) -> True:
    
    # task queue
    tasks_waiting: list[dict[str:int]] = []

    # flags
    has_task: bool = True
    new_arrived: bool = True
    last_task = -1

    time = 1
    while has_task:

        sleep(.1) # delay for debugging

        for task in tasks:
            if task.get('arrival') <= time and task not in tasks_waiting and task.get('timeleft') != 0:
                tasks_waiting.append(task)
        smallest = 0
        if preemp:
            for task_index in range(len(tasks_waiting)):
                if tasks_waiting[task_index].get('timeleft') < tasks_waiting[smallest].get('timeleft'):
                    smallest = task_index
        else:    
            for task_num in range(len(tasks_waiting)):
                for _ in range(len(tasks_waiting) - task_num - 1):

                    if tasks_waiting[task_num].get('arrival') < tasks_waiting[task_num+1].get('arrival'):

                        temp = tasks_waiting[task_num]
                        tasks_waiting[task_num] = tasks_waiting[task_num+1]
                        tasks_waiting[task_num+1] = temp


        
        if len(tasks_waiting) > 0:

            if new_arrived or last_task != tasks_waiting[smallest].get("num"):
                print('-------------------------')
                print(f'Task {tasks_waiting[smallest].get("num")} arrived: ')

                tasks_waiting[smallest]['waiting'] = time - tasks_waiting[smallest]['arrival'] - (tasks_waiting[smallest].get('runtime') - tasks_waiting[smallest].get('timeleft'))
                new_arrived = False

            if tasks_waiting[smallest].get('timeleft') != 0:

                print(f"    Time [ {time} ] -  Timeleft: {tasks_waiting[smallest].get('timeleft')}")
                tasks_waiting[smallest]['timeleft'] -= 1
                last_task = tasks_waiting[smallest].get('num')
                
                if tasks_waiting[smallest].get('timeleft') == 0:
                    new_arrived = True
                    del tasks_waiting[smallest] 

            
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
    sjf(Tasks(), preemp = True) 
    sjf(Tasks(), preemp = False) 