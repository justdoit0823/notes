package com.notes.demo.task;

public class SimpleTaskResult<T> implements TaskResult<T> {

  private T result;

  private boolean success;
  private long executionDuration;
  private long delayDuration;

  public SimpleTaskResult(T result, long executionDuration) {
    this(result, executionDuration, 0L);
  }

  public SimpleTaskResult(T result, long executionDuration, long delayDuration) {
    this(result, executionDuration, delayDuration, true);
  }

  public SimpleTaskResult(T result, long executionDuration, long delayDuration, boolean success) {
    this.result = result;
    this.executionDuration = executionDuration;
    this.delayDuration = delayDuration;
    this.success = success;
  }

  @Override
  public T getTaskResult() {
    return result;
  }

  @Override
  public long getTaskExecutionDuration() {
    return executionDuration;
  }

  @Override
  public long getTaskDelayDuration() {
    return delayDuration;
  }

  @Override
  public boolean isSuccess() {
    return success;
  }
}
