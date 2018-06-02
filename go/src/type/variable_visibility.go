
package main

import "fmt"
import "utils"


type Range struct {

	a int
	b int

}


func main() {

	r1 := Range{1, 100}
	fmt.Println(r1, r1.a, r1.b)

	r2 := utils.Range{10000, 20000}
	fmt.Println(r2, r2.a, r2.b)

}
