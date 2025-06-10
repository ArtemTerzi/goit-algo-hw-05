def binary_search(arr, x):
    step = 0
    low = 0
    high = len(arr) - 1
    mid = 0
    result = None

    while low <= high:
        step += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        else:
            result = arr[mid]
            high = mid - 1

    if result is None:
        return -1
    else:
        return (step, result)


def main():
    arr = [0.5, 1.2, 1.5, 1.8, 2.5, 3.0]
    x = 1.7
    result = binary_search(arr, x)
    if result != -1:
        print(f"Element {x} has the nearest largest value: {result[1]} and was found in {result[0]} iterations")
    else:
        print("Element is not present in array")

if __name__ == "__main__":
    main()