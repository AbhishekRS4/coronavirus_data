import numpy as np
import matplotlib.pyplot as plt

def get_pie_chart_multi_categories(sizes, labels, plot_title, show_percent=False, color_offsets=31, color_offsets_2=101):
    total_values = len(sizes) * 4
    colors = np.arange(0, total_values, 1) / total_values
    colors = np.random.permutation(colors)
    colors = colors.reshape(-1, 4)

    fig = plt.figure(figsize=(12, 12))
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.axis("equal")
    plt.title(plot_title)

    if show_percent:
        percent = 100. * sizes / sizes.sum()
        labels = [f"{i} - {j:1.2f} %" for i, j in zip(labels, percent)]
    else:
        labels = [f"{i} - {j}" for i, j in zip(labels, sizes)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, sizes), key=lambda labels: labels[2], reverse=True))

    plt.legend(patches, labels, loc="best", fontsize=8)
    return fig

def get_bar_chart_single(data, label, title, color):
    fig, axes = plt.subplots(1, 1, figsize=(8, 8))
    axes.set_title(title)
    axes.bar(np.arange(len(data)), data, label=label, color=color)
    axes.legend()
    axes.grid()
    return fig
