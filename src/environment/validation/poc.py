import concurrent.futures, time
import queue

poolx = concurrent.futures.ThreadPoolExecutor(max_workers=1)
poolx.submit(time.sleep, 3)
poolx.submit(time.sleep, 0)   # very fast

print('pending:', poolx._work_queue.qsize(), 'jobs')
print('threads:', len(poolx._threads))
print()

# TODO: make thread safe; work on copy of queue?
print('Estimated Pending Work Queue:')
for num,item in enumerate(poolx._work_queue.queue):
    print('{}\t{}\t{}\t{}'.format(
        num+1, item.fn, item.args, item.kwargs,
        ))

poolx.shutdown(wait=False)