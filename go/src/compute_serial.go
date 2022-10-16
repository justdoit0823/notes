package main


import (
        "fmt"
        "os"
        "strconv"
        "math"
)



func serial_sum(m, n int, r chan float64){

        sum := 0.0
        for i := m; i <= n; i++ {
                sum += 1.0 / float64(i)
        }
        r <- sum
}


func sum_with_ret(x, y int) (z int){
        z = x + y
        return 1
}


func main(){

        if len(os.Args) < 2 {
                fmt.Println("n times number is needed.")
                os.Exit(0)
        }

        n, _ := strconv.Atoi(os.Args[1])

        const partnum = 100000000

        ngo := int(math.Ceil(float64(n) / float64(partnum)))

        r := make(chan float64, ngo)

        for i := 0; i < ngo; i++ {
                start := 1 + i * partnum
                end := int(math.Min(float64(start + partnum), float64(n)))
                go serial_sum(start, end, r)
        }

        sum := 0.0

        for i := 0; i < ngo; i++{
                sum += <- r
        }


        fmt.Printf("%d sum is %f\n", n, sum)
        fmt.Println("sum with ret", sum_with_ret(1, 2))
}
