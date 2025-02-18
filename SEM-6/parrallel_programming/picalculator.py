import math
import time
from threading import Thread
from multiprocessing import Process
from joblib import Parallel, delayed

from tqdm import tqdm


def calculate_pi():
    '''
    '''

    a = {'n': 1, 'n+1': None}
    b = {'n': 1 / math.sqrt(2), 'n+1': None}
    t = {'n': 1 / 4, 'n+1': None}
    p = {'n': 1, 'n+1': None}

    for _ in range(1000):
        a['n+1'] = (a['n'] + b['n']) / 2
        b['n+1'] = math.sqrt(a['n'] * b['n'])
        t['n+1'] = t['n'] - p['n'] * (a['n'] - a['n+1'])**2
        p['n+1'] = 2 * p['n']
        a['n'] = a['n+1']
        b['n'] = b['n+1']
        t['n'] = t['n+1']
        p['n'] = p['n+1']

    pi = (a['n'] + b['n'])**2 / 4 / t['n']
    return pi


def calculate_pi_3000():

    for _ in tqdm(range(3000)):
        result = calculate_pi()

    return result


def calculate_serialy(num=7):

    start_time = time.time()

    for _ in range(num):
        result = calculate_pi_3000()

    print('total time serially:', time.time() - start_time)
    print()
    return result


def calculate_with_threads(num=7):

    start_time = time.time()
    threads = []
    for _ in range(num):
        threads.append(
            Thread(target=calculate_pi_3000)
        )

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('total time using threads:', time.time() - start_time)
    print()
    return 


def calculate_with_processes(num=7):

    start_time = time.time()

    processes = []
    for _ in range(num):
        processes.append(
            Process(target=calculate_pi_3000)
        )

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print('total time parralleely:', time.time() - start_time)
    print()
    return 


def calculate_with_joblib(num=7):

    start_time = time.time()

    results = Parallel(
        n_jobs=num, backend='multiprocessing'
    )(
        delayed(calculate_pi_3000)() for _ in range(num)
    )

    print('total time:', time.time() - start_time)
    print()
    print(results)
    return 
