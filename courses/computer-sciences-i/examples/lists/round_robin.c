#include <stdlib.h>
#include <stdio.h>

typedef struct Process {
    int pid;
    int burst_time;
    int remaining_time;
    struct Process *next;
} Process;

typedef struct {
    Process *processes;
} OperativeSystem;

void insertProcess(OperativeSystem *os, int pid, int burst_time){
    Process *new_process = malloc( sizeof(Process) );
    if(new_process == NULL) {
        puts("Problema creando el nuevo proceso en la memoria");
        return;
    }

    new_process->pid = pid;
    new_process->burst_time = burst_time;
    new_process->remaining_time = burst_time;

    Process *current = os->processes;
    Process *previous = NULL;
    while(current->next != os->processes){
        previous = current;
        current = current->next;
    }

    if(previous == NULL){ //Empty list
        os->processes = new_process;   
    } else {
        previous->next = new_process;   
    }
    new_process->next = os->processes;
}

void displayProcessQueue(OperativeSystem *os){
    Process *current = os->processes;
    puts("=========\nProcesos:\n");
    if(os->processes == NULL){
        puts("No hay procesos en el sistema.");
        return;
    }

    do{
        printf("Proceso %d: Tiempo restante %d", current->pid, current->remaining_time);
        current = current->next;
    } while(current->next != os->processes);
    puts("==========\n");
}

void roundRobin(OperativeSystem *os, int quantum){
    int current_time = 0;

    while(os->processes != NULL){
        Process *current = os->processes;
        
        //int execution_time;
        //if(current->remaining_time < quantum){
        //    execution_time = current->remaining_time;
        //} else {
        //    execution_time = quantum;
        //}
        int execution_time = current->remaining_time < quantum? 
                                        current->remaining_time : quantum;

        printf("PID: %d Tiempo de Simulación: %d hasta %d", 
                        current->pid, current_time, (current_time + execution_time));

        current->remaining_time -= execution_time;
        current_time += execution_time;

        if(current->remaining_time == 0){
            // process finished
            printf("Process %d finished.", current->pid);

            Process *previous = NULL;
            Process *cur = os->processes->next;
            while(cur != current){
                previous = cur;
                cur = cur->next;
            }

            if(previous == NULL){
                os->processes = NULL;
            } else {
                previous->next = current->next;
            }

            free(current);
        } else {
            current = current->next;
        }
        displayProcessQueue(os);
    }
    puts("All the processes have been finished");
}