

package main


import (
	"fmt"
	"time"
	"runtime"
)


func main(){

	fmt.Printf("Current goroutine num %d.\n", runtime.NumGoroutine())

	go func(timeout int){
		time.Sleep(time.Duration(timeout) * time.Second)
		fmt.Printf("This goroutine has slept %d seconds.\n", timeout)
	}(3)

	fmt.Printf("Current goroutine num %d.\n", runtime.NumGoroutine())

	first_warning := true
	s_time := time.Now().Unix()

	for ;; {
		if( first_warning && (time.Now().Unix() - s_time) > 3) {
			fmt.Printf("%d seconds has already gone.\n", 3)
			first_warning = false
		}
	}

}
