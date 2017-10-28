
"""Test gRPC in multiprocess."""

from concurrent import futures
import multiprocessing
import os
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


channel = grpc.insecure_channel('localhost:50051')
stub = helloworld_pb2_grpc.GreeterStub(channel)


def run_call():
  print('Greeter client start.')
  response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)


def child_client_call():
  run_call()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
  server.add_insecure_port('[::]:50051')
  server.start()

  p1 = multiprocessing.Process(target=child_client_call)
  p1.start()

  p1.join(timeout=60)
  if p1.is_alive():
    print('call timeout.')
    p1.terminate()

  server.stop(0)


if __name__ == '__main__':
  serve()
