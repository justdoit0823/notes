
package main


import (
	"fmt"
	"sync"
)


func main() {
	l := sync.Mutex{}

	l.Lock()
	fmt.Println("Hold lock in main goroutine.")

	go func() {
		l.Unlock()
		fmt.Println("Release lock in another goroutine.")
	}()

	l.Lock()
	fmt.Println("Hold lock again.")
	l.Unlock()
}
