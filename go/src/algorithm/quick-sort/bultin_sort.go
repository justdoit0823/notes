
// Builtin sort algorithm in the go.


package main

import "fmt"
import "math/rand"
import "os"
import "sort"
import "strconv"


type IntArray []int


func (a IntArray) Len() int {return len(a)}
func (a IntArray) Swap(i, j int) {a[i], a[j] = a[j], a[i]}
func (a IntArray) Less(i, j int) bool {return a[i] < a[j]}


func main(){
	if len(os.Args) == 1 {
		return
	}

	num, err := strconv.Atoi(os.Args[1])
	if err != nil {
		return
	}

	var elementList []int
	for i := 0; i < num; i++ {
		elementList = append(elementList, int(rand.Int31n(int32(num) * 100)))
	}

	fmt.Println(elementList)

	sort.Sort(IntArray(elementList))
	fmt.Println("After quick sort...")

	fmt.Println(elementList)

}
