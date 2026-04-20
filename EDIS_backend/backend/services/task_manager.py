import uuid
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

TASKS = {}

def submit_task(fn, *args, **kwargs):
    task_id = str(uuid.uuid4())
    future = executor.submit(fn, *args, **kwargs)
    TASKS[task_id] = future
    return task_id

def get_task_result(task_id):
    future = TASKS.get(task_id)
    if not future:
        return {"status": "not_found"}

    if future.done():
        try:
            return {
                "status": "completed",
                "result": future.result()
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    else:
        return {"status": "running"}
