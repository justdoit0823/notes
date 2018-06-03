
// package commnad line entry

package main


import (
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"runtime"
	"sort"
	"time"
)


type CmdArgs struct {
	Connections int
	Duration int
	Threads int
	LatencyStat bool
}


func defineCommand(c *CmdArgs) *flag.FlagSet {
	f := flag.NewFlagSet("hb", flag.ExitOnError)

	f.IntVar(&c.Connections, "c", 0, "Concurrent connections.")
	f.IntVar(&c.Duration, "d", 0, "Benchmark duration.")
	f.IntVar(&c.Threads, "t", 0, "Benchmark threads.")
	f.BoolVar(&c.LatencyStat, "latency", false, "Show latency statistic.")

	return f
}


func initEnvironment(c CmdArgs) {
	if c.Threads > 0 {
		runtime.GOMAXPROCS(c.Threads)
	}
}


type RequestStat struct {
	duration float64
	status int
}


type Worker struct {
	stop chan bool
	requests []RequestStat
}


func NewWorker() *Worker {
	return &Worker{stop: make(chan bool, 1)}
}


func (w *Worker) Run(url string) {
	tr := &http.Transport{MaxIdleConns: 1}
	c := &http.Client{Transport: tr}

	for {
		select {
			case <- w.stop:
				return
			default:
		}

		startTime := time.Now()
		resp, _ := c.Get(url)
		defer resp.Body.Close()
		_, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			continue
		}
		endTime := time.Now()
		w.requests = append(w.requests, RequestStat{float64(endTime.Sub(startTime) / 1000000), resp.StatusCode})
	}
}

func (w *Worker) Stop() {
	w.stop <- true
}


func main() {

	var c CmdArgs
	f := defineCommand(&c)

	err := f.Parse(os.Args[1:])
	if err != nil {
		fmt.Println("Couldn't parse the command arguments.")
	}

	url := f.Arg(0)
	fmt.Println(url)

	if url == "" {
		fmt.Println("URL is needed.")
		return
	}

	if c.Connections <= 0 {
		fmt.Println("Connection must be greater than zero.")
		return
	}

	if c.Duration <= 0 {
		fmt.Println("Duration must be greater than zero.")
		return
	}

	initEnvironment(c)

	var workers []*Worker

	for i := 0; i < c.Connections; i ++ {
		w := NewWorker()
		go w.Run(url)
		workers = append(workers, w)
	}

	t := time.NewTimer(time.Duration(c.Duration) * time.Second)
	<- t.C

	var durations []float64

	for _, w := range workers {
		w.Stop()
		for _, r := range w.requests {
			if r.status == 200 {
				durations = append(durations, r.duration)
			}
		}
	}

	sort.Float64s(durations)

	var total_duration float64
	for _, d := range durations {
		total_duration += d
	}

	n := len(durations)

	fmt.Printf("Finished requests %d within %d seconds, average %d/s.\n", n, c.Duration, n / c.Duration)
	if n > 0 {
		fmt.Printf("Min duration %fms, max duration %fms, avg duration %fms.\n", durations[0], durations[n - 1], total_duration / float64(len(durations)))
	}
}
