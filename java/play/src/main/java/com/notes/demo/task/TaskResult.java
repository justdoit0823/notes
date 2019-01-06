package com.notes.demo.task;

public interface TaskResult<T> {

  T getTaskResult();

  boolean isSuccess();

  long getTaskExecutionDuration();

  long getTaskDelayDuration();

}
