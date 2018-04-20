
// Algorithm parallel quicksort in the go.


package main

import "fmt"
import "math/rand"
import "os"
import "strconv"


func partition(eleList []int, low, high int) (int) {
	pivot := int((low + high) / 2)
	pivotValue := eleList[pivot]

	eleList[pivot], eleList[high] = eleList[high], eleList[pivot]

	lowIndex := low
	for i := low; i < high; i++ {
		if eleList[i] < pivotValue {
			eleList[lowIndex], eleList[i] = eleList[i], eleList[lowIndex]
			lowIndex++
		}
	}

	eleList[lowIndex], eleList[high] = pivotValue, eleList[lowIndex]

	return lowIndex

}


func quick_sort(eleList []int, low, high int, e chan int) {

	pivot := partition(eleList, low, high)

	e1 := make(chan int, 2)

	if pivot > low + 1 {
		go quick_sort(eleList, low, pivot - 1, e1)
	}
	if pivot + 1 < high {
		go quick_sort(eleList, pivot + 1, high, e1)
	}

	if pivot > low + 1 {
		<- e1
	}
	if pivot + 1 < high {
		<- e1
	}

	e <- 1
}


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

	e := make(chan int, 2)

	fmt.Println(elementList)

	quick_sort(elementList, 0, len(elementList) - 1, e)
	<- e
	fmt.Println("After quick sort...")

	fmt.Println(elementList)

}
