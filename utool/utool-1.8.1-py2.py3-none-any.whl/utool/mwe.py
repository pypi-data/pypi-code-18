# import numpy as np


# def worker(mat):
#     return np.linalg.svd(mat)


# def par_svd(args_gen):
#     from concurrent import futures
#     with futures.ProcessPoolExecutor(max_workers=4) as executor:
#         fs_chunk = [executor.submit(worker, args) for args in args_gen]
#         for fs in fs_chunk:
#             yield fs.result()
#     print('EXECUTOR SHUTDOWN')


def main():
    import time
    # for i in range(100):
    while True:
        print('waiting...')
        time.sleep(1)
    # ans = 'y'
    # # ans = input('waiting to start')
    # if ans == 'y':
    #     mats = np.random.rand(1000, 100, 100)
    #     # ser_svds = list(map(worker, mats))
    #     par_svds = list(par_svd(mats))
    #     assert len(par_svds) == 1000
    # # input('waiting to stop')
    # for i in range(10):
    #     print('waiting...')
    #     time.sleep(1)


if __name__ == '__main__':
    main()
