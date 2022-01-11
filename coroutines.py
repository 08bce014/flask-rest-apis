import asyncio


def channel(capacity):
    size = 0
    data = []
    while size <= capacity:
        item = yield
        data.append(item)
        size += 1
    for item in data:
        yield item


async def worker(id: int, jobs: channel, results: channel):
    print(f"starting worker {id}")
    await asyncio.sleep(0)
    for job in jobs:
        await asyncio.sleep(0)
        if job is not None:
            print(f"worker : {id} received job: {job}")
            result = job * job
            results.send(result)


async def main():
    jobs = channel(10)
    results = channel(10)
    next(jobs)
    next(results)

    for i in range(10):
        jobs.send(i)

    task1 = asyncio.create_task(worker(1, jobs, results))
    task2 = asyncio.create_task(worker(2, jobs, results))
    await asyncio.gather(
        task1, task2
    )
    for result in results:
        print(f"result {result}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
