import queue
import threading


# 处理工作请求
class Worker(threading.Thread):
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue

    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)  # get task
                res = callable(*args, **kwds)
                self.resultQueue.put(res)  # put result
            except queue.Empty:
                break


# 线程池管理,创建
class WorkManager:
    def __init__(self, num_of_workers=10):
        # 请求队列
        self.workQueue = queue.Queue()
        # 输出结果的队列
        self.resultQueue = queue.Queue()
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            # 创建工作线程
            worker = Worker(self.workQueue, self.resultQueue)
            # 加入到线程队列
            self.workers.append(worker)

    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            # 从池中取出一个线程处理请求
            worker = self.workers.pop()
            worker.join()
            if worker.is_alive() and not self.workQueue.empty():
                # 重新加入线程池中
                self.workers.append(worker)
        # print('All jobs were complete.')

    def add_job(self, callable, *args, **kwds):
        # 向工作队列中加入请求
        self.workQueue.put((callable, args, kwds))

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)
