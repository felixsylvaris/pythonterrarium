"""
This is script to benchmark speed of various sort methods. 
Minimal working version:
- generete random array of range 0-10 000, size 1000 
- def func to copy, mesure time of sort, and put into times array
- we start with inbuild sort 
- we perform mean, median, std 

DONE:
- generete different array patters, reverse, almost, shifted
- generete global setup variable
- Bubble sort add
- generete dict to store autputs
- generete np converter
- Add more sorting algorithms
- Export results to JSON

TODO:
- Inteligence is knowing how to code, wisdom is understanding when to end

NOT:
- visualization is other module from dat dataframe


"""

# import libraries
import numpy as np
import time
import random
import json  # we need to export them files
import os

# here we declare some global variable as setup
LOW= 0
HIGH = 10000
SIZE = 5000  # this escaletes quickly
TRIALS = 1000
TRIALS_SLOW = 3 # slow algo is really slow

# generete our data list to order 
chaos=np.random.randint(low=LOW,high=HIGH, size=SIZE).tolist()
print('Chaos array example: ', end='')
print(chaos[:10])

reverse = list(range(HIGH-1,HIGH-SIZE-1,-1)) #backwards 
print('Reverse array example: ', end='')
print(reverse[:10])

almost = list(range(LOW + 1, LOW + SIZE + 1)) #almost has some numbers of in the middle
# almost is supposed to be ALMOST ordered just have 2 numbers off, lost sheep case
mid = SIZE // 2

temp = almost[mid]
almost[mid] = almost[0]
almost[0] = temp

temp = almost[mid + 1]
almost[mid + 1] = almost[-1]
almost[-1] = temp
print('Almost ordered array example: ', end='')
print(almost[SIZE//2 -1 : SIZE//2 +9])

dizzy = list(range(LOW, LOW + SIZE)) # dizzy has numbers a couple position off order

WINDOW = 10

for i in range(0, SIZE, WINDOW):
    chunk = dizzy[i:i + WINDOW]
    random.shuffle(chunk)
    dizzy[i:i + WINDOW] = chunk

print('Dizzy array example: ', end='')
print(dizzy[:10])

# make a dict with name of 
tosort_dict={
    "chaos":chaos,
    "reverse": reverse,
    "almost" : almost,
    "dizzy" : dizzy
}

# MAKING ALGORITHMS 
def builtin_sort(arr):
    arr.sort()


def builtin_sorted(arr):
    arr[:] = sorted(arr)

def bubble_sort(arr):
    # this will be bubble sort one day
    
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  

def insertionSort(arr):
    #Shift all larger elements one position to the right traversing the list. SLOW n^2. 
    n = len(arr)
    
    if n <= 1:
        return
    for i in range(1, n):
        key = arr[i]         
        j = i - 1
        while j >= 0 and key < arr[j]: 
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key      

def selectionSort(array):
    # looks for smallest elements if right side of array and puts it on left side. SLOW n^2
    size=len(array)
    for ind in range(size - 1):
        min_index = ind

        for j in range(ind + 1, size):
            if array[j] < array[min_index]:
                min_index = j

        array[ind], array[min_index] = array[min_index], array[ind]

# MERGE SORT BLOCK

def merge(arr, l, m, r):
    # this one is helper func
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[l + i]
    for j in range(n2):
        R[j] = arr[m + 1 + j]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr,lf,r):
    # we are doing some recursion here and divide and conquere
    # we split it in half and then merge 
    
    if lf < r:
        m = lf + (r - lf) // 2
        mergeSort(arr, lf, m)
        mergeSort(arr, m + 1, r)
        merge(arr, lf, m, r)

def mergeSortOut(arr):
    # our func take only array
    # this one should be nlogn fast 
    lft=0
    rgt=len(arr)-1
    mergeSort(arr,lft,rgt)
    return arr 

# QUICK SORT BLOCK
def partition(arr, low, high):
    mid = (low + high) // 2
    arr[mid], arr[high] = arr[high], arr[mid]

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, lows, highs):
    # divide and conquere
    if lows < highs:
        p = partition(arr, lows, highs)
        quick_sort(arr, lows, p - 1)
        quick_sort(arr, p + 1, highs)

def quickSortOut(arr):
    # func standard needs wrapper 
    left=0 
    right=len(arr)-1 
    quick_sort(arr,left,right)
    return arr 

# HEAP SORT BLOCK
def heapify(arr, n, i):
    # helper 
    largest = i    
    l = 2 * i + 1    
    r = 2 * i + 2  

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap max to end
        heapify(arr, i, 0)
    return arr


# we make some lists for easier rotation
algo_list=(builtin_sort, builtin_sorted, bubble_sort,insertionSort, selectionSort, mergeSortOut, quickSortOut, heapSort) # list of algorithm to rotate over, this are funcs 
algo_list=list(algo_list) # cant shuffle tupple
random.shuffle(algo_list) # we shake algorithm around 
slow_algo=("bubble_sort","insertionSort","selectionSort",) #slow algo has long time, comma for list making

# MEASURING FUNC DEF
def mesure(source_,func):
    # this one measures times
    arr=source_.copy()

 

    start = time.perf_counter()
    func(arr)
    elapsed = time.perf_counter() - start
    return elapsed



def review(func, bench):
    # this one prints summarize, but is for single benchmark
    print(
        f"{func.__name__}: "
        f"mean={bench.mean():.8f}s, "
        f"median={np.median(bench):.8f}s, "
        f"std={bench.std():.8f}s"
    )




def benchmark_maker_dict(algo_todo_list, input_data): 
    # we make nested dict, we rotate over algorithms, and for each algo put inside dict with name of order and array of times from measure 

    work_dict={}
    for algo1 in algo_todo_list: #we probably could do __name__ here, but it works that way to.
        algo1str=algo1.__name__ 
        work_dict[algo1str] = {}
        mesure_work={}
        for order,data in input_data.items():
            mesure_work[order]=[]
            if algo1.__name__ in slow_algo:
                for i in range(TRIALS_SLOW):
                    mesure_work[order].append(mesure(data, algo1))
            else:
                for i in range(TRIALS):
                    mesure_work[order].append(mesure(data, algo1))
        work_dict[algo1str]=mesure_work
    return work_dict #do not forget return ans 

benchmarks_done=benchmark_maker_dict(algo_list,tosort_dict)

def np_convert(data):
    # we convert regular arrays inside our dict to np so we can be mean
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = np_convert(value)
        else:
            data[key] = np.array(value)

    return data

benchmarks_done=np_convert(benchmarks_done)

def review_dict(input_dict):
    # this is review generator but from dict
    for algo2 in input_dict.keys():
        for order2, times2 in input_dict[algo2].items():
             print(
                    f"{algo2}: "
                    f"{order2}:"
                    f"mean={times2.mean():.8f}s, "
                    f"median={np.median(times2):.8f}s, "
                    f"std={times2.std():.8f}s"
                )

review_dict(benchmarks_done)
        


# SAVE OUTPUT AS JSON

def json_convert(data):
    result = {}

    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = json_convert(value)
        elif isinstance(value, np.ndarray):
            result[key] = value.tolist()
        else:
            result[key] = value

    return result

def save_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4)

filename = "benchmark_sorting_output.json"

default_dir = os.path.dirname(os.path.abspath(__file__)) # take dir of script file
os.chdir(default_dir) #set working directory on script dir
save_to_file(json_convert(benchmarks_done),filename)




# RIP poor pc. But it prints numbers. 

"""
# MESURE TIME
bench1 = []
bench2 = []
bench3= []

for i in range(1000):
    bench1.append(mesure(chaos, builtin_sort))

for i in range(1000):
    bench2.append(mesure(chaos, builtin_sorted))

for i in range(TRIALS_SLOW):
    bench3.append(mesure(chaos, bubble_sort))
    

bench1 = np.array(bench1)
bench2 = np.array(bench2)
bench3 = np.array(bench3)

review(builtin_sort, bench1)
review(builtin_sorted, bench2)
review(bubble_sort, bench3)

"""
