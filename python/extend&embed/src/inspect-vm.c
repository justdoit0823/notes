
#include <stdio.h>
#include <stdlib.h>
#include <sys/uio.h>
#include <dlfcn.h>

#include <errno.h>
#include <string.h>

#include <Python.h>
#include <frameobject.h>

extern int errno;


struct pyruntimestate {
  int initialized;
  int core_initialized;
  PyThreadState *finalizing;

  struct pyinterpreters {
    PyThread_type_lock mutex;
    PyInterpreterState *head;
    PyInterpreterState *main;
    int64_t next_id;
  } interpreters;
};

int read_runtime_state(int pid, const void * addr, struct pyruntimestate * runtime) {
  struct iovec local[4], remote[1];
  struct pyruntimestate pyruntime;
  int size = sizeof(pyruntime);

  local[0].iov_base = &pyruntime.initialized;
  local[0].iov_len = 8;
  local[1].iov_base = &pyruntime.core_initialized;
  local[1].iov_len = 8;
  local[2].iov_base = &pyruntime.finalizing;
  local[2].iov_len = 8;
  local[3].iov_base = &pyruntime.interpreters;
  local[3].iov_len = sizeof(struct pyinterpreters);

  remote[0].iov_base = addr + 0x555de0;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 4, remote, 1, 0);
  if (nread > 0) {
    *runtime = pyruntime;
  }

  return nread;
}


int read_interpreter_state(int pid, const void * addr, PyInterpreterState * state) {
  struct iovec local[2], remote[1];
  PyInterpreterState interpreterState;
  int size = sizeof(PyInterpreterState);

  local[0].iov_base = &interpreterState.next;
  local[0].iov_len = 8;
  local[1].iov_base = &interpreterState.tstate_head;
  local[1].iov_len = 8;

  remote[0].iov_base = addr;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 2, remote, 1, 0);
  if (nread > 0) {
    *state = interpreterState;
  }

  return nread;
}

int read_thread_state(int pid, const void * addr, PyThreadState * state) {
  struct iovec local[4], remote[1];
  PyThreadState threadState;
  int size = sizeof(PyThreadState);

  local[0].iov_base = &threadState.prev;
  local[0].iov_len = 8;
  local[1].iov_base = &threadState.next;
  local[1].iov_len = 8;
  local[2].iov_base = &threadState.interp;
  local[2].iov_len = 8;
  local[3].iov_base = &threadState.frame;
  local[3].iov_len = 8;

  remote[0].iov_base = addr;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 4, remote, 1, 0);
  if (nread > 0) {
    *state = threadState;
  }

  return nread;
}


int read_frame_object(int pid, const void * addr, PyFrameObject * object) {
  struct iovec local[1], remote[1];
  PyFrameObject frame;
  int size = sizeof(PyFrameObject);

  local[0].iov_base = &frame;
  local[0].iov_len = size;
  remote[0].iov_base = addr;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 1, remote, 1, 0);
  if (nread > 0) {
    *object = frame;
  }

  return nread;
}


int read_code_object(int pid, const void * addr, PyCodeObject * object) {
  struct iovec local[1], remote[1];
  PyCodeObject code;
  int size = sizeof(PyCodeObject);

  local[0].iov_base = &code;
  local[0].iov_len = size;
  remote[0].iov_base = addr;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 1, remote, 1, 0);
  if (nread > 0) {
    *object = code;
  }

  return nread;
}

int read_type(int pid, const void * addr, PyTypeObject * object) {
  struct iovec local[1], remote[1];
  PyTypeObject t;
  int size = sizeof(t);

  local[0].iov_base = &t;
  local[0].iov_len = size;
  remote[0].iov_base = addr;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 1, remote, 1, 0);
  if (nread > 0) {
    *object = t;
  }

  return nread;
}

int read_native_str(int pid, const void * addr, char * str, int size) {
  struct iovec local[1], remote[1];

  local[0].iov_base = str;
  local[0].iov_len = size;
  remote[0].iov_base = addr;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 1, remote, 1, 0);

  return nread;
}


int main(int argc, char * argv[]) {
  if (argc < 3) {
    printf("Both pid and base address are needed.\n");
    return 0;
  }

  int pid = atoi(argv[1]);
  long base_addr = atol(argv[2]);
  printf("process %d, %lx.\n", pid, (void *)base_addr);

  struct pyruntimestate runtime;
  int nread = read_runtime_state(pid, base_addr, &runtime);

  printf("read %d bytes, %s.\n", nread, strerror(errno));
  printf("inited %d, %lx.\n", runtime.initialized, runtime.interpreters.head);

  PyInterpreterState interpreterState;
  read_interpreter_state(pid, runtime.interpreters.head, &interpreterState);

  PyThreadState * tState = interpreterState.tstate_head;
  while (tState != NULL) {
    PyThreadState threadState;

    int nread = read_thread_state(pid, tState, &threadState);
    printf("read %d bytes, %s, %lx.\n", nread, strerror(errno), threadState.frame);

    tState = threadState.next;

    if (threadState.interp == runtime.interpreters.head) {
      printf("yes....\n");
    } else {
      printf("address %lx, %lx.\n", threadState.interp, runtime.interpreters.head);
    }

    if(threadState.frame == NULL) {
      printf("thread state address %lx.\n", tState);
      continue;
    }

    PyFrameObject frame;
    read_frame_object(pid, threadState.frame, &frame);

    PyCodeObject code;
    read_code_object(pid, frame.f_code, &code);

    PyTypeObject t;
    read_type(pid, code.ob_base.ob_type, &t);

    char name_buf[128];
    read_native_str(pid, t.tp_name, name_buf, 128);
    printf("code type's name is %s.\n", name_buf);
  }

  return 0;
}
