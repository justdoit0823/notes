
"""MPI point to point communication."""

import random

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


def transfer_python_object():
    """Transfer python object."""
    if rank == 0:
        for idx in range(1, 10):
            data = {'a': random.random(), 'b': random.random()}
            comm.send(data, dest=1, tag=idx)
    elif rank == 1:
        for idx in range(1, 10):
            data = comm.recv(source=0, tag=idx)
            print(idx, data)


def broadcast_python_object():
    """Broadcast python object."""
    if rank == 0:
        data = {
            'key1' : [7, 2.72, 2+3j],
            'key2' : ( 'abc', 'xyz')
        }
    else:
        data = None

    data = comm.bcast(data, root=0)
    print(rank, data)


def main():
    transfer_python_object()
    broadcast_python_object()


if __name__ == '__main__':
    main()
