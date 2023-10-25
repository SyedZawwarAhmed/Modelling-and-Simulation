from texttable import Texttable
from statistics import mean
from datetime import datetime
import pandas as pd
import plotly.express as px

class Patient:
    def __init__(self, patient_id, arrival_time, burst_time, priority, service_time):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.time_left = service_time
        self.is_arrived = False
        self.is_ready = False
        self.start_time = 0
        self.end_time = 0
        self.completion_time = 0
        self.turn_around_time = 0
        self.wait_time = 0
        self.response_time = 0
        self.utilization_time = 0
        self.response_ratio = 0
        self.start_times = []
        self.end_times = []

    def decrement_time_left(self):
        self.time_left -= 1

    def set_start_time(self, time_passed):
        self.start_time = time_passed

    def set_end_time(self, time_passed):
        self.end_time = time_passed

    def set_completion_time(self, time_passed):
        self.completion_time = time_passed

    def set_turn_around_time(self):
        self.turn_around_time = self.completion_time - self.arrival_time

    def set_wait_time(self):
        self.wait_time = self.turn_around_time - self.burst_time

    def set_response_time(self, time_passed):
        self.response_time = time_passed - self.arrival_time

    def set_utilization_time(self):
        self.utilization_time = self.burst_time / self.turn_around_time

    def append_start_times(self, time_passed):
        self.start_times.append(time_passed)

    def append_end_times(self, time_passed):
        self.end_times.append(time_passed)

    def set_response_ratio(self, time_passed):
        self.response_ratio = (
            (time_passed - self.arrival_time) + self.burst_time) / self.burst_time
        

def check_should_service_proceed(patient_list):
    for patient in patient_list:
        if patient.time_left > 0:
            return True
    return False

def sort_patients_according_to_shortest_arrival(patient_list):
    return sorted(patient_list, key=lambda patient: patient.arrival_time, reverse=False)

def sort_patients_according_to_highest_priority(patient_list):
    return sorted(patient_list, key=lambda patient: patient.priority, reverse=False)

def get_patients_of_same_highest_priority(patient_list, maximum_priority):
    patients_of_same_highest_priority = []
    for patient in patient_list:
        if patient.priority == maximum_priority:
            patients_of_same_highest_priority.append(patient)
    return patients_of_same_highest_priority

def print_patient_table(patient_list):
    table = Texttable()
    table_rows = [["patient_id", "arrival_time", "service_time", "priority", "start_time", "end_time",
                   "turn_around_time", "wait_time", "response_time"]]
    for patient in patient_list:
        new_row = [patient.patient_id, patient.arrival_time, patient.burst_time, patient.priority, patient.start_time, patient.end_time,
                   patient.turn_around_time, patient.wait_time, patient.response_time]
        table_rows.append(new_row)
    table.add_rows(table_rows)
    table.set_max_width(200)
    print(table.draw())


def print_patient_average_table(patient_list):
    table = Texttable()
    table_rows = [["average_completion_time",
                   "average_turn_around_time", "average_wait_time", "average_response_time", "average_utilization_time"]]
    average_completion_time = mean(
        [patient.completion_time for patient in patient_list])
    average_turn_around_time = mean(
        [patient.turn_around_time for patient in patient_list])
    average_wait_time = mean([patient.wait_time for patient in patient_list])
    average_response_time = mean(
        [patient.response_time for patient in patient_list])
    average_utilization_time = mean(
        [patient.utilization_time for patient in patient_list])

    new_row = [average_completion_time, average_turn_around_time,
               average_wait_time, average_response_time, average_utilization_time]
    table_rows.append(new_row)
    table.add_rows(table_rows)
    table.set_max_width(200)
    print(table.draw())

def seconds_to_timestamp(seconds):
    timestamp = datetime.fromtimestamp(seconds)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def draw_gantt_chart(patient_list):
    data_frame_list = []
    # df = pd.DataFrame([dict(Patient=patient.patient_id, Start=seconds_to_timestamp(
    #     patient.start_time), Finish=seconds_to_timestamp(patient.end_time)) for patient in patient_list])

    x_axis_tickvals = []
    for patient in patient_list:
        for i in range(len(patient.start_times)):
            data_frame_list.append(dict(Patient=str(patient.patient_id), Start=seconds_to_timestamp(
                patient.start_times[i]), Finish=seconds_to_timestamp(patient.end_times[i])))
            x_axis_tickvals.append(seconds_to_timestamp(patient.start_times[i]))
            x_axis_tickvals.append(seconds_to_timestamp(patient.end_times[i]))
    df = pd.DataFrame(data_frame_list)

    fig = px.timeline(df, x_start="Start", x_end="Finish",
                      y="Patient", color="Patient")
    # fig.update_yaxes(autorange="reversed")
    fig.update_layout(xaxis=dict(title='Time Passed (seconds)', tickformat='%S', tickvals=x_axis_tickvals), yaxis=dict(title='Patients', tickvals=[patient.patient_id for patient in patient_list]))
    fig.show()

def serve_highest_priority_first(patients):
    ready_queue = []
    time_passed = 0

    print('\nServing Patients according to Highest Priority.')
    ran_patient = None
    while check_should_service_proceed(patients):
        ready_queue = []
        for patient in patients:
            if patient.arrival_time <= time_passed and patient.time_left > 0:
                ready_queue.append(patient)

        if len(ready_queue) == 0:
            time_passed += 1
        else:
            sorted_ready_queue_according_to_highest_priority = sort_patients_according_to_highest_priority(
                ready_queue)
            maximum_priority = sorted_ready_queue_according_to_highest_priority[0].priority

            patients_of_same_highest_priority = get_patients_of_same_highest_priority(
                sorted_ready_queue_according_to_highest_priority, maximum_priority)

            sorted_ready_queue_according_to_shortest_arrival = sort_patients_according_to_shortest_arrival(
                patients_of_same_highest_priority)

            running_queue = [
                sorted_ready_queue_according_to_shortest_arrival[0]]

            if not ran_patient or ran_patient != running_queue[0]:
                running_queue[0].append_start_times(time_passed)
                if ran_patient:
                    ran_patient.append_end_times(time_passed)
                ran_patient = running_queue[0]
            if not ran_patient.is_ready:
                ran_patient.set_response_time(time_passed)
                ran_patient.set_start_time(time_passed)
                ran_patient.is_ready = True
            time_passed += 1
            ran_patient.time_left -= 1
            if ran_patient.time_left == 0:
                ran_patient.set_end_time(time_passed)
                ran_patient.set_completion_time(time_passed)
                ran_patient.set_turn_around_time()
                ran_patient.set_wait_time()
                ran_patient.set_utilization_time()
    if len(ran_patient.start_times) > len(ran_patient.end_times):
        ran_patient.append_end_times(time_passed)

    total_service_time = 0
    for patient in patients:
        total_service_time += patient.burst_time

    utlization_time = total_service_time / time_passed

    if utlization_time < 0 or utlization_time > 1:
        print("Invalid mean, utilization time is out of range.")
        return
    
    draw_gantt_chart(patients)

    print(f'Utilization Time:- {utlization_time}')

    print("Final Patient Table")
    print_patient_table(patients)
    print_patient_average_table(patients)
    # for patient in patients:
    #     print(patient.patient_id)
    #     print("start times", patient.start_times)
    #     print("end times", patient.end_times)
    #     print()