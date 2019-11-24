import json
import matplotlib.pyplot as plt

filename = "walk.log"

gtype = "magnet"
with open(filename) as f:
    data = json.loads(f.read())

x = []
axes = [[],[],[]]
i = 0
for sensor in data["sensors"]:
    if i % 10 == 0:
        x.append(i)
        for j in range(3):
            axes[j].append(float(sensor[gtype][j]))
    #else:
    #    for j in range(3):
    #        axes[j][len(axes[j]) - 1] += float(sensor[gtype][j])
    i = i + 1

plt.figure()
plt.subplot(111)
plt.plot(x, axes[0])
plt.plot(x, axes[1])
plt.plot(x, axes[2])
plt.yscale('linear')
plt.grid(True)

plt.show()

