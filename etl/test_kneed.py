import matplotlib.pyplot as plt

from kneed import KneeLocator

print('reading')
x: list = []
y: list = []
with open('text_mining.txt', 'r') as file_in:
    for line in file_in:
        x_entry, y_entry = [
            float(value.strip())
            for value in line.split('\t')
        ]
        x.append(x_entry)
        y.append(y_entry)

print('calculating')
kneedle = KneeLocator(x, y, S=1.0, curve='concave', direction='decreasing', online=True)

print(kneedle.knee, kneedle.knee_y)

figsize = (12, 6)

plt.figure(figsize=figsize)
plt.title("Divergence Relevancy to Text Mining")
plt.plot(x[:1000], y[:1000], "b", label="divergence")
plt.vlines(
    kneedle.knee, plt.ylim()[0], plt.ylim()[1], linestyles="--", label="knee"
)
plt.legend(loc="best")
plt.savefig("text_mining.png")
