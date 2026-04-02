"""def merge(left, right):
    sorted_list = []
    i=j=0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left(i))
            print("sorted_list left: ", sorted_list)
            i += 1
        else:
            sorted_list.append(right[j])
            print("sorted_list right: ", sorted_list)
            j += 1
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    print("mid: ", mid)
    print("left_half: ", arr[:mid])
    print("right_half: ", arr[mid:])
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    return merge(left_half, right_half)
unodered_data = [10,56,354,645,23,76,8,2]
sorted_data = merge_sort(unodered_data)
print(sorted_data)"""

"""def selection_sort (data:list) -> list:
    result = data.copy()
    n = len(result)
    for i in range(n):
        print (f"Pass {i}: {result}")
        min_idx = i
        print ("min_idx in i loop:", min_idx)
        for j in range (i+1, n):
            if result[j] < result[min_idx]:
                print ("min_idx in j loop updated to: ", min_idx)
        result[i], result[min_idx] = result[min_idx], result[i]
        print(f"After swap {i}: {result}")
    return result 
distances = [3.5, 1.2, 4.8, 0.9, 2.1]
sorted_distances = selection_sort(distances)
print(sorted_distances)"""

"""objects = [
    {"id": "A", "distance": 3.5},
    {"id": "B", "distance": 1.2},
    {"id": "C", "distance": 4.8},
    {"id": "D", "distance": 0.9},
    {"id": "E", "distance": 5.0},
]
sorted_objects = sorted(objects, key = lambda obj: obj["distance"])
print(sorted_objects[0])
print(sorted_objects)
distances = [3.5,1.2,4.8,0.9,2.1]
print (sorted(distances))
print (sorted(distances, reverse = True))"""

robot_distances = [2.3, 0.8, 4.1, 1.5, 3.7]
sorted_dist = sorted(robot_distances) # sorted(robot_distances, reverse = True)
print (sorted_dist)
print(f"Closest robot at: {sorted_dist[0]}m") # sorted_dist[-1]

