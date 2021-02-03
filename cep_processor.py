# coding=utf-8
import collections
import fnmatch
import multiprocessing

try:
    import queue
except ImportError:
    import Queue as queue

import time


# 호가변경시 출력
def stk_echo(serieses, key, dat):
    print('STK:%s, dat:%s' % (key[3:], dat))  # stk slice

def fut_echo(serieses, key, dat):
    futtype, code = key[:4], key[5:]
    print('%4s) %-8s [%s]' % (futtype, code, dat))  # fut slice

def opt_echo(serieses, key, dat):
    print('OPT:%s, dat:%s'% (key[3:], dat))  # opt slice

def tmp_echo(serieses, key, dat):
    print("('%s', '%s', )," % (key, dat))  # fut slice


def gen_eproc(observers=[]):
    e_proc = EventProcessor()
    e_proc.add_observer(['stk*_A*'], stk_echo)
    e_proc.add_observer(['fut*_*'], fut_echo)
    e_proc.add_observer(['#*'], tmp_echo)
    # e_proc.add_observer(['fut*_*'], fut_echo)
    # e_proc.add_observer(['opt*_*'], opt_echo)
    # e_proc.start()
    return e_proc


class EventProcessor(multiprocessing.Process):
    def __init__(self, deque_size=4096):
        super(EventProcessor, self).__init__()
        self.q_buf = multiprocessing.Queue()  #입력 버퍼
        self.o_buf = multiprocessing.Queue()  # 옵저버 버퍼
        self.observers = dict()  # 옵저버집합
        self.observer_list = []  # 옵저버 리스트
        self.serieses = dict()  # 시계열집합
        self.DQ_SIZE = deque_size

    def add_observer(self, key_patterns, callable):
        self.o_buf.put((key_patterns,callable))

    def push(self, key, data):
        ts = time.time()
        self.q_buf.put((ts, key, data))

    def run(self):
        while True:
            try:
                # 입력큐에서 하나 가져온다.
                itm = self.q_buf.get(timeout=1)
                ts = itm[0]  # push 메서드에서 넣은 순서
                key = itm[1]
                dat = itm[2]

                # 신규 옵저버 등록
                while self.o_buf.empty() == False:
                    self.observer_list.append(self.o_buf.get())

                # 키 확인, 없으면 추가
                if key not in self.serieses:
                    # 시계열에 해당 키 추가
                    self.serieses [key] = collections.deque(maxlen=self.DQ_SIZE)
                    self.observers[key] = []
                    # 모든 옵저버
                    for obv in self.observer_list:
                        patterns = obv[0]
                        callable = obv[1]
                        # 각 옵저버의 키패턴 unix-shell style로 패턴비교
                        for pat in patterns:
                            if fnmatch.fnmatch(key, pat):
                                self.observers[key].append(callable)

                # 덱에 원소 추가
                self.serieses[key].appendleft((ts, dat))

                # Notify
                for callback in self.observers[key]:
                    callback(self.serieses, key, dat)

            except queue.Empty:
                continue


if __name__ == "__main__":
    print('EventProcessor Test')
