#!/usr/bin/env python3

"""Rendering output"""

import shutil
import datetime
import texttable


class AutowidthTexttable(texttable.Texttable):

    def __init__(self, *args, **kwargs):
        if not 'max_width' in kwargs:
            termsize = shutil.get_terminal_size((80, 24))
            kwargs['max_width'] = termsize.columns

        super().__init__(*args, **kwargs)


def show_activities(timed, day=None):

    HEADER = ['Customer', 'Project', 'Task', 'Comment', 'Duration']

    table = AutowidthTexttable()

    activities = timed.activities(day)

    table.header(HEADER)

    rows = [
            [
                act.task.project.customer.name if act.task else "",
                act.task.project.name if act.task else "",
                act.task.name if act.task else "",
                act.comment,
                act.current_duration()
            ]
            for act
            in activities]


    table.add_rows(rows, header=False)

    total = sum([act.current_duration() for act in activities],
                datetime.timedelta(0))

    table.add_row(['', '', '', 'TOTAL', total])

    print(table.draw() + "\n")

def show_reports(timed, day=None):
    table = AutowidthTexttable()

    HEADER = ['Customer', 'Project', 'Task', 'Comment', 'Duration']

    reports = timed.reports(day)
    table.header(HEADER)

    table.add_rows(
        ([
            rep.task.project.customer.name,
            rep.task.project.name,
            rep.task.name,
            rep.comment,
            rep.duration
        ]
        for rep in reports),

        header=False
    )

    total = sum([r.duration for r in reports],
                datetime.timedelta(0))

    table.add_row(['', '', '', 'TOTAL', total])

    print(table.draw() + "\n")


def show_user_status(timed):
    "Show the user's status (Employment, overtime balance, etc)"

    user = timed.user()
    employments = timed.employments()
    emp = current_employment(employments)
    worktime_balance = timed.worktime_balance()

    print("User: %s %s (id=%s)" % (user.first_name, user.last_name, user.id))
    print("      Employment: %s%% (%s per day)" % (emp.percentage, emp.worktime_per_day))
    print("      Balance:    %s" % worktime_balance.balance)


def current_employment(employments):
    now = datetime.datetime.now()
    for emp in employments:
        start_date = datetime.datetime.strptime(emp.start_date, '%Y-%m-%d')
        try:
            end_date   = datetime.datetime.strptime(emp.end_date  , '%Y-%m-%d')
        except:
            end_date = datetime.datetime.now()

        if start_date < now and end_date >= now:
            return emp
