

interface CounterOperator {

    public void add();

    public int getValue();

}

class SyncCounter implements CounterOperator {

    private int cnt = 0;

    public synchronized void add() {
	cnt += 1;
    }

    public int getValue() {
	return cnt;
    }

}

class VolatileCounter implements CounterOperator {

    private volatile int cnt = 0;

    public void add() {
	cnt += 1;
    }

    public int getValue() {
	return cnt;
    }

}

class MutateThread extends Thread {

    private CounterOperator c;
    private int num = 0;

    public MutateThread(CounterOperator c, int n) {
	this.c = c;
	num = n;
    }

    public void run() {
	for(int i = 0; i < num; i++) c.add();
    }

}


public class ConcurrentMutate {

    public static void main(String[] args) {
	int threadNum = 10;
	int opNum = 10;
	String counterType;

	if(args.length < 1) {
	    System.out.println("Counter type is needed.");
	    return;
	}

	counterType = args[0];

	if(args.length > 1) threadNum = Integer.parseInt(args[1]);
	if(args.length > 2) opNum = Integer.parseInt(args[2]);

	CounterOperator c;
	if(counterType.equals("sync")) {
	    c = new SyncCounter();
	} else {
	    c = new VolatileCounter();
	}

	MutateThread[] threads = new MutateThread[threadNum];

	for(int i = 0; i < threadNum; i++) {
	    threads[i] = new MutateThread(c, opNum);
	}

	for(MutateThread t: threads) {
	    t.start();
	}

	for(MutateThread t: threads) {
	    try {
		t.join();
	    } catch (InterruptedException e) {
		System.out.println(e);
		continue;
	    }
	}

	System.out.println(c.getValue());

    }
}
