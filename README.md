# python_learning



## Part 3: Time and Space Complexity (Big O)

Big O notation describes how the runtime or memory usage of an algorithm grows as the input size (`n`) increases.

### Common Time Complexities

* **O(1) - Constant:** Time is independent of input size
* **O(log n) - Logarithmic:** Input size reduces each step
* **O(n) - Linear:** Time grows with input
* **O(n²) - Quadratic:** Common in nested loops

---

### Time Calculation Example

```python
def example(data):
    # O(1)
    print(data[0]) 

    # O(n)
    for item in data:
        print(item)

    # O(n^2)
    for i in data:
        for j in data:
            print(i, j)
```

---

## Part 4: Deep Dive into Space Complexity

Space complexity refers to the total amount of memory space an algorithm uses relative to input size `n`.

### 1. Auxiliary Space vs Total Space

* **Auxiliary Space:** Temporary space used by the algorithm
* **Total Space Complexity:** Input space + auxiliary space

---

### 2. O(1) - Constant Space

Memory does not grow with input size.

```python
def find_max(numbers):
    max_val = numbers[0]
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
```

---

### 3. O(n) - Linear Space

Memory grows with input size.

```python
def get_squares(numbers):
    squares = []
    for n in numbers:
        squares.append(n * n)
    return squares
```

---

## Part 5: Best Practices and Learning Resources

### 1. Time-Space Trade-off

In real-world scenarios:

* Faster programs often use more memory
* Memory-efficient programs may run slower

**Example:**
Using a dictionary (hash map) gives `O(1)` lookup but increases space usage.

---

### 2. Efficiency Summary Table

| Complexity  | Notation | Scalability                          |
| ----------- | -------- | ------------------------------------ |
| Constant    | O(1)     | Excellent: Performance never changes |
| Logarithmic | O(log n) | Great: Efficient for large datasets  |
| Linear      | O(n)     | Good: Scales with data               |
| Quadratic   | O(n²)    | Poor: Slows quickly with large data  |

---
