
package main


import "fmt"
import "reflect"


func main() {
	i := 1
	var t interface{}

	t = i

	switch t.(type) {
	case int:
		fmt.Println("i's type is int, and value is", t.(int))
	default:
		fmt.Println("no type.")
	}

	fmt.Println("i's type is", reflect.TypeOf(t), ", and value is", reflect.ValueOf(t))
}
