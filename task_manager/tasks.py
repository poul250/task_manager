import argparse
from colorama import Fore
import os
import subprocess

import config

TASKS_DIR = os.path.join(config.TASK_MANAGER_PATH, 'tasks')


def preapre_environment():
    os.makedirs(TASKS_DIR, exist_ok=True)


def add(args):
    tasks_ids = []
    for path in os.listdir(TASKS_DIR):
        tasks_ids.append(int(os.path.split(path)[-1]))

    last_task_id = 0 if not tasks_ids else max(tasks_ids)
    new_task_id = last_task_id + 1
    subprocess.run([config.TEXT_EDITOR, os.path.join(TASKS_DIR, str(new_task_id))])


def lst(args):
    task_ids = sorted(int(path) for path in os.listdir(TASKS_DIR))

    for task_id in task_ids:
        with open(os.path.join(TASKS_DIR, str(task_id)), 'r') as task_text:
            print(f'{Fore.GREEN}task #{task_id}:{Fore.RESET}')
            print(task_text.read())


def done(args):
    task_id = args.task_id
    task_path = os.path.join(TASKS_DIR, str(task_id))

    task_ids = sorted(int(task) for task in os.listdir(TASKS_DIR))

    removed = False
    for task in task_ids:
        if removed:
            os.rename(os.path.join(TASKS_DIR, str(task)), os.path.join(TASKS_DIR, str(task-1)))
        elif task == task_id:
            os.remove(task_path)
            removed = True


def edit(args):
    task_id = args.task_id
    task_path = os.path.join(TASKS_DIR, str(task_id))

    if os.path.isfile(task_path):
        subprocess.run([config.TEXT_EDITOR, task_path])


def _swap(task1, task2):
    task1_path = os.path.join(TASKS_DIR, str(task1))
    task2_path = os.path.join(TASKS_DIR, str(task2))
    if os.path.exists(task1_path) and os.path.exists(task2_path):
        tmp_path = os.path.join(TASKS_DIR, 'tmp_task')
        os.rename(task1_path, tmp_path)
        os.rename(task2_path, task1_path)
        os.rename(tmp_path, task2_path)


def up(args):
    _swap(args.task_id, args.task_id - 1)


def down(args):
    _swap(args.task_id, args.task_id + 1)


def swap(args):
    _swap(args.task_id1, args.task_id2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='tasks', description='Tasks manager')
    parser.set_defaults(func=lst)
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser('list')
    list_parser.set_defaults(func=lst)

    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=add)

    edit_parser = subparsers.add_parser('edit')
    edit_parser.add_argument('task_id', type=int)
    edit_parser.set_defaults(func=edit)

    done_parser = subparsers.add_parser('done')
    done_parser.add_argument('task_id', type=int)
    done_parser.set_defaults(func=done)

    up_parser = subparsers.add_parser('up')
    up_parser.add_argument('task_id', type=int)
    up_parser.set_defaults(func=up)

    down_parser = subparsers.add_parser('down')
    down_parser.add_argument('task_id', type=int)
    down_parser.set_defaults(func=down)

    down_parser = subparsers.add_parser('swap')
    down_parser.add_argument('task_id1', type=int)
    down_parser.add_argument('task_id2', type=int)
    down_parser.set_defaults(func=swap)

    args = parser.parse_args()

    preapre_environment()
    args.func(args)
