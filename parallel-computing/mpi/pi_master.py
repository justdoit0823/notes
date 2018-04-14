
"""Compute pi master."""

import sys

from mpi4py import MPI
import numpy


def compute_pi():
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=['pi_worker.py'], maxprocs=5)

    N = numpy.array(10000, 'i')
    print(N)
    comm.Bcast([N, MPI.INT], root=MPI.ROOT)
    PI = numpy.array(0.0, 'd')
    comm.Reduce(None, [PI, MPI.DOUBLE], op=MPI.SUM, root=MPI.ROOT)
    print(PI)

    comm.Disconnect()


def main():
    compute_pi()


if __name__ == '__main__':
    main()
