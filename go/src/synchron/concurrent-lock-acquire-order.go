
package main


import "flag"
import "fmt"
import "sync"
import "time"


func main() {
	starvationFlag := flag.Bool("starvation", false, "enable lock starvation test.")
	flag.Parse()

	var wg sync.WaitGroup
	var x []int

	ready := false
	l := &sync.Mutex{}	
	c := sync.NewCond(&sync.Mutex{})

	for i := 0; i < 5; i++ {

		wg.Add(1)
		go func(b int){
			c.L.Lock()
			for ; !ready; {
				c.Wait()
			}
			c.L.Unlock()
			fmt.Println("Start", b / 100, "goroutine at", time.Now())

			for i := 0; i < 10; i++ {
				l.Lock()

				x = append(x, b + i)
				if *starvationFlag {
					time.Sleep(time.Duration(100) * time.Microsecond)
				}

				l.Unlock()
			}
			wg.Done()

		}(i * 100)
	}

	ready = true
	c.Broadcast()

	wg.Wait()	
	fmt.Println(x)
}
