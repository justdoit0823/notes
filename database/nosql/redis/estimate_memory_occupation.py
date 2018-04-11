
"""Estimate redis memory occupation module."""

import string

import click
import random
import redis


TOTAL_LETTERS = string.ascii_letters + string.digits
key_len_list = (3, 10, 20, 40, 70, 100)
val_len_list = (10, 20, 30, 40, 50, 100, 200, 300, 500, 1000, 2000)


def get_random_string(length):
    """Return random fixed length string."""
    return ''.join(random.choice(TOTAL_LETTERS) for idx in range(length))


def call_log(func):
    """Trace function call decorator."""

    def innerWapper(*args, **kwargs):
        print('\n=============', func.__name__, 'begin', '===========')
        print('key', 'val', 'element')
        func(*args, **kwargs)
        print('=============', func.__name__, 'end', '=============')

    return innerWapper


@call_log
def estimate_stage(conn, func):
    """Estimate key space."""
    for key_len in key_len_list:
        key = get_random_string(key_len)
        for val_len in val_len_list:
            element_space = func(conn, key, val_len)
            print(key_len, val_len, element_space)


def estimate_key_space(conn, key, val_len):
    """Estimate key space."""
    val = get_random_string(val_len)

    conn.set(key, val)
    object_info = conn.debug_object(key)
    memory_space = object_info['serializedlength']

    conn.delete(key)

    return memory_space


def estimate_list_space(conn, key, val_len):
    """Estimate list space."""
    for idx in range(100):
        val = get_random_string(val_len)

        conn.lpush(key, val)
        object_info = conn.debug_object(key)
        memory_space = object_info['serializedlength']
        if idx == 0:
            first_space = memory_space

    conn.delete(key)

    return (memory_space - first_space) / 100

def estimate_hash_space(conn, key, val_len):
    """Estimate hash space."""
    for idx in range(100):
        val = get_random_string(val_len)
        field = 'field{0}'.format(idx)

        conn.hset(key, field, val)
        object_info = conn.debug_object(key)
        memory_space = object_info['serializedlength']
        if idx == 0:
            first_space = memory_space

    conn.delete(key)

    return (memory_space - first_space) / 100


def estimate_set_space(conn, key, val_len):
    """Estimate set space."""
    for idx in range(100):
        val = get_random_string(val_len)

        conn.sadd(key, val)
        object_info = conn.debug_object(key)
        memory_space = object_info['serializedlength']
        if idx == 0:
            first_space = memory_space

    conn.delete(key)

    return (memory_space - first_space) / 100


def estimate_sorted_set_space(conn, key, val_len):
    """Estimate sorted set space."""
    for idx in range(100):
        val = get_random_string(val_len)

        conn.zadd(key, val, idx * 100.0)
        object_info = conn.debug_object(key)
        memory_space = object_info['serializedlength']
        if idx == 0:
            first_space = memory_space

    conn.delete(key)

    return (memory_space - first_space) / 100


@click.group()
def main():
    pass


@main.command('estimate', help='start estimation.')
@click.argument('host', type=str, default='127.0.0.1')
@click.argument('port', type=int, default=6379)
@click.argument('db', type=int, default=11)
def run(**kwargs):
    host = kwargs['host']
    port = kwargs['port']
    db = kwargs['db']
    conn = redis.Redis(host, port, db)

    estimate_stage(conn, estimate_key_space)
    estimate_stage(conn, estimate_list_space)
    estimate_stage(conn, estimate_hash_space)
    estimate_stage(conn, estimate_set_space)
    estimate_stage(conn, estimate_sorted_set_space)


if __name__ == '__main__':
    main()
