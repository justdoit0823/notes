
package main


import "flag"
import "fmt"
import "net"
import "net/http"
import "net/rpc"
import "os"
import "time"


type Person struct {
	firstName string
	lastName string
}

type Args struct {
	Greeting string
}


func (p *Person) Hello(args *Args, reply *string) error {
	fmt.Printf("Receive %s.\n", args.Greeting)
	*reply = "Hello"
	return nil
}


func startRPCServer(addr string) {
	p := &Person{"Go", "RPC"}
	rpc.Register(p)
	rpc.HandleHTTP()

	l, e := net.Listen("tcp", addr)
	if e != nil {
		fmt.Println("start RPC server failed.")
	}

	http.Serve(l, nil)
}


func startRPC(client *rpc.Client, addr string) {
	args := &Args{"Hello from go RPC client."}
	reply := ""

	err := client.Call("Person.Hello", args, &reply)
	if err != nil {
		fmt.Println("call Hello RPC failed.", err)
		return
	}

	fmt.Printf("receive reply %s.\n", reply);

}


type CmdArgs struct {
	addr string
	duration int
	serverMode bool
	clientMode bool
}


func defineCommandFalgs(c *CmdArgs) *flag.FlagSet {
	f := flag.NewFlagSet("go-rpc", flag.ExitOnError)

	f.StringVar(&c.addr, "addr", "", "RPC server addr.")
	f.IntVar(&c.duration, "duration", 0, "run duration.")
	f.BoolVar(&c.serverMode, "server", false, "run mode.")
	f.BoolVar(&c.clientMode, "client", false, "run mode.")

	return f
}


func main() {
	var c CmdArgs
	f := defineCommandFalgs(&c)

	f.Parse(os.Args[1:])

	if c.serverMode && c.clientMode {
		f.PrintDefaults()
		return
	}

	if c.addr == "" {
		f.PrintDefaults()
		return
	}

	if c.serverMode {
		startRPCServer(c.addr)
		return
	}

	if !c.clientMode {
		f.PrintDefaults()
		return
	}

	if c.duration <= 0 {
		f.PrintDefaults()
		return
	}

	client, err := rpc.DialHTTP("tcp", c.addr)
	if err != nil {
		fmt.Printf("Dial RPC server %s failed.\n", c.addr)
		return
	}

	t := time.NewTimer(time.Duration(c.duration) * time.Second)
	sc := make(chan int, 10)

	for i := 0; i < 10; i++ {
		go func () {
			stop := false
			for ; !stop; {
				select {
				case <- sc:
					stop = true
					break
				default:
					break
				}

				startRPC(client, c.addr)
			}
		}()
	}

	<- t.C
}
