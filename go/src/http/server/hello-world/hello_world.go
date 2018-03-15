// hello world server

package main

import "fmt"
import "log"
import "math/rand"
import "net/http"
import "os"
import "strconv"
import "strings"
import "time"

func main() {
	var addr string

	if len(os.Args) == 1 {
		addr = strings.Join([]string{"127.0.0.1", strconv.Itoa(int(50000 + rand.Int31n(2000)))}, ":")
	} else {
		addr = os.Args[1]
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello world.")
	})

	server := &http.Server{
		Addr:           addr,
		ReadTimeout:    5 * time.Second,
		WriteTimeout:   5 * time.Second,
		MaxHeaderBytes: 1 << 16,
	}

	fmt.Printf("Runing server at %s...\n", addr)
	log.Print(server.ListenAndServe())
}
