# Threading in Python

Threading is a separate flow of execution. This means that a program will have processes running simultaneously, however, for most Python 3 implementations, the threads merely appear to be executing at the same time.
It's easy to assume that different processors are running your program independently at the same time and there is some truth to this assumption. Threads may run on different processors however **they will not be running at the same time**.

If a task spends most of its time waiting for external events then its a good idea to implement threading however, if the task is CPU intensive then threading may not be of much use at all.

<br/>

## Threading example
```python
import logging
import threading
import time


def thread_function(name):
	logging.info("Thread %s: starting", name)
	time.sleep(2)
	logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
	format = "%(asctime)s: %(messages)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
	logging.info("Main   : before creating thread")
	
	# This is how you create a thread
	x = threading.Thread(target=thread_function, args=(1,))
	x.start()
	logging.info("Main   : wait for the thread to finish")
	# x.join()
	logging.info("Main   : all done")

```

This is how the thread is created:
```python
x = threading.Thread(target=thread_function, args=(1,))
```

<br/>

# Daemon Threads

A daemon is simply a program that runs in the background. In python threading, **daemon** has a different meaning - a daemon thread shuts down when the program exits. A program will wait for non-daemonic threads to finish before it shuts down however daemonic threads are shutdown immediately when the main program exits.
This behaviour of threads can easily be modified by setting the ```daemon = True``` during the instantiation of the thread.


```python
x = threading.Thread(target=thread_function, args=(1,), daemon=True)
```

You'll notice that the final output of the program is missing.

<br/>

## <code>join()</code> a Thread 

What if you want a thread to stop **without exiting the program**? Enter the ```join()``` method. The ```join()``` method of a thread is used to the thread to pause and wait for another thread to finish.


<br/>

# The <code>ThreadPoolExecutor</code>

The <code>ThreadPoolExecutor</code> is another way to start a group of threads. It is part of the standard library in <code>concurrent.futures</code>. The easiest way to create the <code>ThreadPoolExecutor</code> is by using a context manager.

```python
import concurrent.futures

# some code

if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

	with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		executor.map(thread_funtion, range(3))



```

<br/>

# Race conditions
When writing threaded programs, a **race condition** can occur if two or more threads try to access a share piece of data or a resource.

<br/>

## An example of a race condition

```FakeDatabase``` keeps track a single number.


```python
import logging
import time


class FakeDatabase:

	def __init__(self):
		self.value = 0


	def update(self, name):
		logging.info("Thread %s: starting update", name)
		local_copy = self.value
		local_copy += 1
		time.sleep(0.1)
		self.value = local_copy
		logging.info("Thread %s: finishing update", name)



# How to use the Fakedatabase
if __name__ == "__main__":
	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

	# instantiate fake database
	database = FakeDatabase()
	logging.info("Testing update. Starting value is %d.", database.value)

	# Create ThreadPoolExecutor
	# The program creates a ThreadPoolExecutor with two threads and then calls .submit() on each of them, telling them to run database.update()
	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
		for index in range(2):
			executor.submit(database.update, index)

	logging.info("Testing update. Ending value %d.", database.value)


```
<br/>

## The ```.submit()``` signature
```python
.submit(function, *args, **kwargs)
```

Visit https://realpython.com/intro-to-python-threading/ for a full explanation of a race condition. 

<br/>

# REMEMBER!
The operating system can swap which thread is running *at any time*. A thread can be swapped out after any of these small instructions. This means that **a thread can be put to sleep to let another thread run in the middle of a Python statement**.

<br/>

# Synchronization using a Lock

A Lock is one of the several ways to stop a race condition. To solve the race condition above, we'll have to find a way to let a single thread complete its execution before another starts, and locks are the perfect for this. *Only one thread can have a ```Lock``` at a time. Another thread that wants access to the ```Lock``` has to wait until the owner releases it.

The ```my_lock.acquire()``` and ```my_lock.release()``` methods are used to get and release locks respectively. If a lock is already held, then the thread has to wait until the lock is released. Python's ```Lock``` will also operate as a **context-manager**, so you can use the ```with``` statement.


```python

class FakeDatabase:
	def __init__(self):
		self.value = 0

		# Lock is initialized in the unlocked state
		self._lock = threading.Lock()

	# The thread running this function will hold on to that the Lock until it is completely finished updating the database. 
	def locked_update(self, name):
		logging.info("Thread %s: starting update", name)
		logging.debug("Thread %s about to lock", name)
		
		with self._lock:
			logging.debug("Thread %s has lock", name)
			local_copy = self.value
			local_copy += 1
			time.sleep(0.1)
			self.value = local_copy
			logging.debug("Thread %s about to release lock", name)
		logging.debug("Thread %s after release", name)
		logging.info("Thread %s: finishing update", name)


# Try running this with the Fakedatabase above
```

<br/>

# Producer-Consumer Threading

Refer to ```producer_consumer_threading.py```.









		
