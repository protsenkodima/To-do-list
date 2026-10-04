from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from starlette import status


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

class TaskCreateSchema(BaseModel):
    title: str
    description: str = None
app = FastAPI()

task_list = [
    {
    "id": 1,
    "title": "Task 1",
    "description": "Task 1",
    "completed": False
    }
]

@app.post("/task", status_code=status.HTTP_201_CREATED)
def create_task(new_task: TaskCreateSchema) -> Response:
    new_task = {
        "id": len(task_list) + 1,
        "title": new_task.title,
        "description": new_task.description,
        "completed": False
    }
    task_list.append(new_task)
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return task_list

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int) -> TaskSchema:
    for task in task_list:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> Response:
    for task in task_list:
        if task["id"] == task_id:
            task_list.remove(task)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")