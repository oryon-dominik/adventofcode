# Beauty of python
data = [int(e) for e in open('01.data', "r").read().split('\n')]  # dirty open
increasing = sum([1 for index, _ in enumerate(data) if index > 0 and data[index] > data[index - 1]])
print(f"Result: {increasing}")
