
package main


import (
	"fmt"
	"runtime"
)


func main(){
	fmt.Printf("%d cpus on this machine.\n", runtime.NumCPU())
}
