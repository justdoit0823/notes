
Go
===

[Go](https://golang.org/) is an open source programming language that makes it easy to build simple, reliable, and efficient software.
And goroutine is a part of making concurrency easy to use.


Sample code
-----------

```go
package main


import (
	"fmt"
	"time"
	"runtime"
)


func main(){

	ch := make(chan int, 1)
	fmt.Printf("Current goroutine num %d.\n", runtime.NumGoroutine())

	go func(timeout int){
		ch <- 1
		time.Sleep(time.Duration(timeout) * time.Second)
		fmt.Printf("This goroutine has slept %d seconds.\n", timeout)
	}(3)

	<- ch
	fmt.Printf("Current goroutine num %d.\n", runtime.NumGoroutine())

	for ;; {}
}

```

The above snippet is my test program.

```bash
```
