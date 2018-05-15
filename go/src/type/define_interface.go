
package main

import "fmt"
import "strconv"


type Point struct {
	x, y int
}

func (p Point) Repr() string {
	return "(" + strconv.Itoa(p.x) + ", " + strconv.Itoa(p.y) + ")"
}

func (p Point) Shape() {
	fmt.Println(p.Repr())
}


type Line struct {
	a, b Point
}

func (l Line) Shape() {
	fmt.Printf("from point %s to point %s.\n", l.a.Repr(), l.b.Repr())
}


type Triangle struct {
	a, b, c Point
}


func (t Triangle) Shape() {
	fmt.Printf("from point %s to point %s to %s.\n", t.a.Repr(), t.b.Repr(), t.c.Repr())
}


type Drawer interface {

	Shape()
}

func main() {
	
	p1 := Point{1, 2}
	p2 := Point{2, 3}
	p3 := Point{3, 3}

	l1 := Line{p1, p2}
	t1 := Triangle{p1, p2, p3}

	iList := []Drawer{l1, t1}

	for _, drawer := range iList {
		drawer.Shape()
	}
}
