import queue
import threading


Thread_NUM = 10  # thread number
PAGE_SIZE = 100  # page number
Q_SHARE = queue.Queue()


class Workers(threading.Thread):

    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index

    def run(self):
        while True:
            index = self.index.get()
            """
            do something
            """
            self.index.task_done()


def main():
    for i in range(Thread_NUM):
        thread = Workers(Q_SHARE)
        thread.daemon = True
        thread.start()
    for i in range(PAGE_SIZE):
        Q_SHARE.put(i)
    Q_SHARE.join()

if __name__ == '__main__':
    main()
