
// Algorithm quicksort in the go.


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


func quick_sort(eleList []int, low, high int) {

	pivot := partition(eleList, low, high)

	if pivot > low + 1 {
		quick_sort(eleList, low, pivot - 1)
	}
	if pivot + 1 < high {
		quick_sort(eleList, pivot + 1, high)
	}
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

	for _, val := range(elementList) {
		fmt.Println(val)
	}

	quick_sort(elementList, 0, len(elementList) - 1)
	fmt.Println("After quick sort...")


	for _, val := range(elementList) {
		fmt.Println(val)
	}

}
