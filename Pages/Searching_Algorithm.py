import streamlit as st
import time
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Searching Algorithms", layout="wide")
st.title("🔍 Searching Algorithms")

# --- Helper Functions ---
def linear_search(arr, target):
    steps = []
    for i, val in enumerate(arr):
        steps.append((i, val))
        if val == target:
            return i, steps
    return -1, steps

def binary_search(arr, target):
    steps = []
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        steps.append((left, mid, right))
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps

def visualize_linear(arr, steps, target):
    fig, ax = plt.subplots()
    for i, val in steps:
        colors = ['green' if j == i and arr[j] == target else 'orange' if j == i else 'skyblue' for j in range(len(arr))]
        ax.clear()
        ax.bar(range(len(arr)), arr, color=colors)
        st.pyplot(fig)
        time.sleep(0.3)

def visualize_binary(arr, steps, target):
    fig, ax = plt.subplots()
    for left, mid, right in steps:
        colors = ['lightgrey'] * len(arr)
        for i in range(left, right + 1):
            colors[i] = 'orange'
        colors[mid] = 'green'
        ax.clear()
        ax.bar(range(len(arr)), arr, color=colors)
        st.pyplot(fig)
        time.sleep(0.3)

# --- Inputs ---
st.sidebar.header("Search Input")
arr_input = st.sidebar.text_input("Enter array", "4, 2, 7, 1, 9, 3")
target_input = st.sidebar.text_input("Target value", "3")
algorithm = st.sidebar.radio("Algorithm", ["Linear Search", "Binary Search"])

try:
    arr = list(map(int, arr_input.split(',')))
    target = int(target_input)
except:
    st.error("Invalid input format.")
    st.stop()

# --- Run Search ---
if st.button("Run Search"):
    start = time.time()
    if algorithm == "Linear Search":
        idx, steps = linear_search(arr, target)
        visualize_linear(arr, steps, target)
        st.write("Time Complexity: O(n)")
    else:
        arr.sort()
        idx, steps = binary_search(arr, target)
        visualize_binary(arr, steps, target)
        st.write("Time Complexity: O(log n)")
    end = time.time()

    st.write(f"Execution Time: {end-start:.5f} sec")
    if idx != -1:
        st.success(f"Found at index {idx}")
    else:
        st.warning("Not Found")