# for example puroposes and to compare with the rust and go solutions..
with open('01.data', "r") as file:
    data = [int(entry) for entry in file.read().split('\n')]

increasing = 0
for measurement, depth in enumerate(data):
    if measurement > 0 and data[measurement] > data[measurement - 1]:
        increasing += 1

print(f"Result: {increasing}")
