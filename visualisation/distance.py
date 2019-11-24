import json
import matplotlib.pyplot as plt

filename = "wozek.log"

gtype = "acc"
with open(filename) as f:
    data = json.loads(f.read())

x = []
speed = [0,0,0]
dist = [0,0,0]
axes = [[],[],[]]
i = 0
for sensor in data["sensors"]:
    i = i + 1
    if i < 2000: continue
    for j in range(3):
        speed[j] = (speed[j] + float(sensor[gtype][j]) * 0.01) * 0.999
        dist[j] += speed[j] * 0.01
        if i % 10 == 0:
            axes[j].append(dist[j])
    if i % 10 == 0:
        x.append(i)

plt.figure()
plt.subplot(111)
plt.plot(x, axes[0])
plt.plot(x, axes[1])
plt.plot(x, axes[2])
plt.yscale('linear')
plt.grid(True)

plt.show()

