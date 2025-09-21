import timeit
import dis
import sys
import gc

def bubble_sort(arr):
    """Bubble sort implementation - O(n²)"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quicksort(arr):
    """Quicksort implementation - O(n log n) average"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def benchmark_sorts():
    """Benchmark bubble sort vs quicksort"""
    test_data = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    
    print("=== Performance Benchmark ===")
    
    # Bubble sort benchmark
    bubble_time = timeit.timeit(
        lambda: bubble_sort(test_data.copy()), 
        number=1000
    )
    print(f"Bubble sort (1000 runs): {bubble_time:.6f}s")
    
    # Quicksort benchmark
    quick_time = timeit.timeit(
        lambda: quicksort(test_data.copy()), 
        number=1000
    )
    print(f"Quicksort (1000 runs): {quick_time:.6f}s")
    
    print(f"Quicksort is {bubble_time/quick_time:.2f}x faster")

def analyze_bytecode():
    """Analyze bytecode of functions using dis module"""
    print("\n=== Bytecode Analysis ===")
    
    def simple_add(a, b):
        return a + b
    
    def complex_add(a, b):
        result = a
        result += b
        return result
    
    print("Simple add function bytecode:")
    dis.dis(simple_add)
    
    print("\nComplex add function bytecode:")
    dis.dis(complex_add)

def memory_demo():
    """Demonstrate reference counting and garbage collection"""
    print("\n=== Memory Management Demo ===")
    
    class Node:
        def __init__(self, value):
            self.value = value
            self.ref = None
    
    # Reference counting demo
    node1 = Node(1)
    print(f"Reference count for node1: {sys.getrefcount(node1) - 1}")  # -1 vì getrefcount tạo thêm 1 ref
    
    node2 = node1  # Tăng reference count
    print(f"Reference count after assignment: {sys.getrefcount(node1) - 1}")
    
    # Circular reference demo (cần garbage collector)
    node1.ref = node2
    node2.ref = node1
    print("Created circular reference")
    
    # Force garbage collection
    collected = gc.collect()
    print(f"Garbage collector collected {collected} objects")

def gil_simulation():
    """Simulate GIL impact with CPU-bound task"""
    import threading
    import time
    
    print("\n=== GIL Impact Demo ===")
    
    def cpu_bound_task(n):
        """CPU-intensive task"""
        count = 0
        for i in range(n):
            count += i * i
        return count
    
    # Single-threaded execution
    start = time.time()
    result1 = cpu_bound_task(1000000)
    result2 = cpu_bound_task(1000000)
    single_time = time.time() - start
    print(f"Single-threaded: {single_time:.4f}s")
    
    # Multi-threaded execution (should be slower due to GIL)
    start = time.time()
    thread1 = threading.Thread(target=cpu_bound_task, args=(1000000,))
    thread2 = threading.Thread(target=cpu_bound_task, args=(1000000,))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    multi_time = time.time() - start
    print(f"Multi-threaded: {multi_time:.4f}s")
    print(f"Multi-threading is {multi_time/single_time:.2f}x slower (GIL overhead)")

if __name__ == "__main__":
    benchmark_sorts()
    analyze_bytecode()
    memory_demo()
    gil_simulation()
    
    print("\n=== Hands-on Exercises ===")
    print("1. Modify bubble_sort to count comparisons and swaps")
    print("2. Analyze bytecode of list comprehension vs for loop")
    print("3. Create memory leak demo and fix it")
    print("4. Compare threading vs multiprocessing for CPU tasks")