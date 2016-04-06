import gevent
import gevent.monkey
gevent.monkey.patch_socket()

PAGE_SIZE = 100  # page number


def worker(args):
    """
    do something
    """


def main():
    threads = []
    for i in range(PAGE_SIZE):
        threads.append(gevent.spawn(worker, i))
    gevent.joinall(threads)


if __name__ == '__main__':
    main()
