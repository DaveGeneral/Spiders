import multiprocessing


POOL_NUM = 8  # process number
PAGE_SIZE = 100  # page number


def Workers(args):
    """
    do something
    """


def main():
    pool = multiprocessing.Pool(POOL_NUM)
    pool.map(Workers, range(PAGE_SIZE))
    # map_async, apply, apply_async
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
