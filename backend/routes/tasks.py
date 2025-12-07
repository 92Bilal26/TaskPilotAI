"""Task CRUD routes"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from db import get_session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskResponse])
async def get_tasks(session: Session = Depends(get_session), user_id: str = None):
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: Session = Depends(get_session), user_id: str = None):
    db_task = Task(**task.dict(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, session: Session = Depends(get_session), user_id: str = None):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404)
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate, session: Session = Depends(get_session), user_id: str = None):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404)
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, session: Session = Depends(get_session), user_id: str = None):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404)
    session.delete(task)
    session.commit()

@router.patch("/{task_id}/complete")
async def toggle_task(task_id: str, session: Session = Depends(get_session), user_id: str = None):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404)
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
