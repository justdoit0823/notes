
import requests
import sys
import csv
import multiprocessing
import grequests


def check_urls(url_list):
    d = {'err': []}
    for url in url_list:
        curl = 'http://' + url
        try:
            ret = requests.get(curl, timeout=(10, 10))
        except:
            # import traceback
            # traceback.print_exc()
            d['err'].append(url)
        else:
            try:
                d[ret.status_code].append(url)
            except KeyError:
                d[ret.status_code] = [url]
    return d


def async_check_urls(url_list, request_size=128):
    d = {'err': []}
    greq = grequests.imap(
        (grequests.get(
            'http://' + url, timeout=(10, 10)) for url in url_list),
        size=request_size)
    while True:
        try:
            res = next(greq)
        except StopIteration:
            break
        except:
            d['err'].append(res.url)
        else:
            try:
                d[res.status_code].append(res.url)
            except KeyError:
                d[res.status_code] = [res.url]
            
    return d


def load_urls(f):
    return list(set([i[1] for i in list(csv.reader(open(f)))]))


def worker_job(urls, queue):
    d = check_urls(urls)
    queue.put(d)


def schedule_worker(worker_tasks, max_workers=8):
    d = {}
    worker_list = []
    tasks = len(worker_tasks)
    avg_tasks = tasks // max_workers

    for i in range(max_workers):
        queue = multiprocessing.Queue()
        b = i * avg_tasks
        e = b + avg_tasks
        if i == max_workers - 1:
            e = tasks
        w = multiprocessing.Process(
            target=worker_job, args=(worker_tasks[b:e], queue))
        w.start()
        worker_list.append((w, queue))

    while worker_list:
        pop_list = []
        for i, (w, q) in enumerate(worker_list):
            try:
                dp = q.get_nowait()
            except:
                continue
            else:
                for k, v in dp.items():
                    try:
                        d[k] += v
                    except KeyError:
                        d[k] = v

                w.join()
                pop_list.append(i)

        if not pop_list:
            import time
            time.sleep(1)
            continue
        for j, k in enumerate(pop_list):
            worker_list.pop(k - j)
    return d


def main():

    urls = load_urls(sys.argv[1])
    # d = check_urls(urls)
    # d = schedule_worker(urls, 32)
    d = async_check_urls(urls, 1000)
    for k in d:
        print('status:', k)
        for u in d[k]:
            print(u)
        print('\n')


if __name__ == '__main__':

    main()
