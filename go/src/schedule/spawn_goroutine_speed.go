
// Test spawning goroutine speed.

package main


import "fmt"
import "os"
import "strconv"
import "time"


func foo () {}


func main() {
	testNum := 10

	if len(os.Args) > 1 {
		inputNum, err := strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Println("Invalid number.")
		}

		testNum = inputNum
	}

	start := time.Now()

	for i := 0; i < testNum; i++ {
		go foo()
	}

	t := time.Now()
	elapsed := t.Sub(start)

	fmt.Printf("Spawn %d goroutines in %d ms.\n", testNum, elapsed)
}
