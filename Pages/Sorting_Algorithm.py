import streamlit as st
import time
import matplotlib.pyplot as plt
import random
import numpy as np

st.set_page_config(page_title="Sorting Algorithms", layout="wide")
st.title("🔃 Sorting Algorithms")

# ---------- Sorting Functions with Steps ----------

def bubble_sort(arr):
    a = arr.copy()
    steps = []
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            steps.append(a.copy())
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    steps.append(a.copy())
    return a, steps

def selection_sort(arr):
    a = arr.copy()
    steps = []
    for i in range(len(a)):
        min_idx = i
        for j in range(i + 1, len(a)):
            steps.append(a.copy())
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    steps.append(a.copy())
    return a, steps

def insertion_sort(arr):
    a = arr.copy()
    steps = []
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
            steps.append(a.copy())
        a[j + 1] = key
        steps.append(a.copy())
    return a, steps

def merge_sort(arr):
    steps = []
    def merge(a, l, m, r):
        L = a[l:m+1]
        R = a[m+1:r+1]
        i = j = 0
        k = l
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            k += 1
            steps.append(a.copy())
        while i < len(L):
            a[k] = L[i]
            i += 1
            k += 1
            steps.append(a.copy())
        while j < len(R):
            a[k] = R[j]
            j += 1
            k += 1
            steps.append(a.copy())

    def mergeSort(a, l, r):
        if l < r:
            m = (l + r) // 2
            mergeSort(a, l, m)
            mergeSort(a, m + 1, r)
            merge(a, l, m, r)

    a = arr.copy()
    mergeSort(a, 0, len(a) - 1)
    return a, steps

def counting_sort(arr):
    a = arr.copy()
    steps = []
    max_val = max(a)
    count = [0] * (max_val + 1)
    for num in a:
        count[num] += 1
        steps.append(a.copy())
    index = 0
    for i, c in enumerate(count):
        while c > 0:
            a[index] = i
            index += 1
            c -= 1
            steps.append(a.copy())
    return a, steps

def radix_sort(arr):
    def counting_sort_exp(a, exp, steps):
        n = len(a)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            idx = (a[i] // exp) % 10
            count[idx] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            idx = (a[i] // exp) % 10
            output[count[idx] - 1] = a[i]
            count[idx] -= 1
            i -= 1

        for i in range(n):
            a[i] = output[i]
            steps.append(a.copy())

    a = arr.copy()
    steps = []
    max_val = max(a)
    exp = 1
    while max_val // exp > 0:
        counting_sort_exp(a, exp, steps)
        exp *= 10
    return a, steps

def heapify(a, n, i, steps):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and a[l] > a[largest]:
        largest = l
    if r < n and a[r] > a[largest]:
        largest = r
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        steps.append(a.copy())
        heapify(a, n, largest, steps)

def heap_sort(arr):
    a = arr.copy()
    steps = []
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i, steps)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        steps.append(a.copy())
        heapify(a, i, 0, steps)
    return a, steps

# ---------- Visualization ----------
def visualize_sorting(steps):
    fig, ax = plt.subplots()
    for step in steps:
        ax.clear()
        ax.bar(range(len(step)), step, color='skyblue')
        st.pyplot(fig)
        time.sleep(0.3)

# ---------- UI ----------
st.sidebar.header("Sort Input")
arr_input = st.sidebar.text_input("Enter array (comma-separated)", "5, 3, 8, 4, 2")
generate = st.sidebar.button("Generate Random Array")
algorithm = st.sidebar.selectbox(
    "Select Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Counting Sort", "Radix Sort", "Heap Sort"]
)

if generate:
    size = st.sidebar.slider("Size", 5, 30, 10)
    arr = random.sample(range(1, 100), size)
else:
    try:
        arr = list(map(int, arr_input.split(',')))
    except:
        st.error("Invalid array format")
        st.stop()

if st.button("Run Sorting"):
    start = time.time()
    if algorithm == "Bubble Sort":
        sorted_arr, steps = bubble_sort(arr)
        complexity = "Best: O(n), Avg/Worst: O(n²)"
    elif algorithm == "Selection Sort":
        sorted_arr, steps = selection_sort(arr)
        complexity = "Best/Worst/Avg: O(n²)"
    elif algorithm == "Insertion Sort":
        sorted_arr, steps = insertion_sort(arr)
        complexity = "Best: O(n), Worst: O(n²)"
    elif algorithm == "Merge Sort":
        sorted_arr, steps = merge_sort(arr)
        complexity = "Best/Avg/Worst: O(n log n)"
    elif algorithm == "Counting Sort":
        sorted_arr, steps = counting_sort(arr)
        complexity = "Best/Avg/Worst: O(n + k)"
    elif algorithm == "Radix Sort":
        sorted_arr, steps = radix_sort(arr)
        complexity = "Best/Avg/Worst: O(nk)"
    elif algorithm == "Heap Sort":
        sorted_arr, steps = heap_sort(arr)
        complexity = "Best/Avg/Worst: O(n log n)"
    else:
        st.error("Unsupported algorithm selected.")
        st.stop()

    end = time.time()
    visualize_sorting(steps)
    st.write(f"Time Complexity: {complexity}")
    st.write(f"Execution Time: {end - start:.5f} sec")
    st.success(f"Sorted Array: {sorted_arr}")
