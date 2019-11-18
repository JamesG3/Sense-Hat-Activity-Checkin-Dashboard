import time
from copy import deepcopy
from datetime import date
from sense_hat import SenseHat

from Record import Record
from Action import Action
from Display import Display

import settings


cur_date = date.today()

record_file = './data/record.csv'
record = Record(record_file)
action = Action()
display = Display()
s = SenseHat()

cur_act_index = 0
cur_act = record.acts[cur_act_index]
title_flag = 1
sleep_flag = 0
cur_month_flag = 1

Y = settings.YELLOW
O = settings.NOTHING
B = settings.BLUE
R = settings.RED
P = settings.PURPLE
W = settings.WHITE
G = settings.GREEN


def update(how='no'):
    '''
    Update the matrix to display
    Input: 
        offset_m - Int - how many months prev the current month
        how - 'prev' / 'reset' / 'next' / 'no'
    Return: (final_matrix_display, cur_day)
    '''
    cur_m_flg = record.update_date(how)
    status_matrix, cur_day, last_day = record.get_cur_status_matrix(cur_act)
    month_matrix = record.get_month_matrix()

    # set color for each func zone
    status_matrix_display = [G if p else O for p in status_matrix]
    status_matrix_display[last_day] = W
    month_matrix_display = [Y if p else O for p in month_matrix]

    final_matrix_display = status_matrix_display + month_matrix_display
    return final_matrix_display, cur_day, cur_m_flg


def get_status2(status1, cur_day):
    status2 = deepcopy(status1)
    status2[cur_day-1] = R
    return status2

final_matrix_display_1, cur_day, cur_month_flag = update()
final_matrix_display_2 = get_status2(final_matrix_display_1, cur_day)


event_start_time = time.time()
while True:
    if cur_date != date.today():
        cur_date = date.today()
        record.update_date('reset')

    if sleep_flag:
        s.clear()
        while True:
            time.sleep(7)
            events = s.stick.get_events()
            if action.get_action(events) == 'sleep':
                sleep_flag = 0
                break


    if title_flag:
        display.show_msg(cur_act)
        title_flag = 0
        final_matrix_display_1, cur_day, cur_month_flag = update()
        final_matrix_display_2 = get_status2(final_matrix_display_1, cur_day)

    event_time = time.time()
    # collect events every 1.5s
    if (event_time - event_start_time) > 1.5:
        event_start_time = event_time
        events = s.stick.get_events()
        action_name = action.get_action(events)

        if events:

            if cur_month_flag:
                # only in the current month can (un)checkin events
                if action_name == 'update_checkin':
                    final_matrix_display_1, cur_day, cur_month_flag = update()
                    final_matrix_display_2 = get_status2(final_matrix_display_1, cur_day)

                    # revert current status if clicked, save changes
                    if final_matrix_display_1[cur_day-1] == O:
                        final_matrix_display_1[cur_day-1] = G
                        record.flip_cur_status(cur_act, 1)
                    else:
                        final_matrix_display_1[cur_day-1] = O
                        record.flip_cur_status(cur_act, 0)

            # switch to another activity
            if action_name == 'prev_page':
                if cur_act_index > 0:
                    cur_act_index -= 1
                    cur_act = record.acts[cur_act_index]
                title_flag = 1
            
            elif action_name == 'next_page':
                if cur_act_index < record.act_num-1:
                    cur_act_index += 1
                    cur_act = record.acts[cur_act_index]
                title_flag = 1

            elif action_name == 'next_month':
                final_matrix_display_1, cur_day, cur_month_flag = update('next')
                final_matrix_display_2 = get_status2(final_matrix_display_1, cur_day)

            elif action_name == 'prev_month':
                final_matrix_display_1, cur_day, cur_month_flag = update('prev')
                final_matrix_display_2 = get_status2(final_matrix_display_1, cur_day)

            elif action_name == 'reset':
                final_matrix_display_1, cur_day, cur_month_flag = update('reset')
                final_matrix_display_2 = get_status2(final_matrix_display_1, cur_day)

            # turn off the dashboard
            elif action_name == 'sleep':
                sleep_flag = 1
    
    if cur_month_flag:
        display.blink(final_matrix_display_1, final_matrix_display_2)
    else:
        display.display_status(final_matrix_display_1)

