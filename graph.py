import numpy as np
import matplotlib.pyplot as plt


def bar_chart(data, date, legend, pict_name, other_names=None):
    # data - матрица, тип ndarray, число строк = длина legend, число столбцов = длина date
    # date - список со строками
    # legend - список со строками
    # pict_name - строка
    # other_names - список со строками [название графика, название оси x, название оси y]
    if not data or not legend or not date:
        return False
    if other_names is None:
        other_names = ['' for i in range(3)]
    data = np.array(data).transpose()
    n_series = len(legend)
    n_observations = len(date)
    x = np.arange(n_observations)
    fig, ax = plt.subplots(figsize=(18.5, 10.5))
    width_cluster = 0.7
    width_bar = width_cluster/n_series
    for n in range(n_series):
        x_positions = x+(width_bar*n)-width_cluster/2
        bar = ax.bar(x_positions, data[:,n], width_bar, align='edge', label=legend[n%3])
        for rect in bar:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
    ax.set_title(other_names[0])
    ax.set_xlabel(other_names[1])
    ax.set_ylabel(other_names[2])
    ax.set_xticks(x)
    ax.set_xticklabels(date)
    ax.legend()
    try:
        plt.savefig('img/' + pict_name + '.png', bbox_inches='tight', dpi=80)
        # plt.savefig('img/' + pict_name + '.png', bbox_inches='tight', dpi=80)
        return True
    except Exception as e:
        return False




def line_chart(data, date, legend, pict_name, other_names=None):
    if other_names is None:
        other_names = ['' for i in range(3)]
    fig, ax = plt.subplots(figsize=(18.5, 10.5))
    for row, leg in zip(data, legend):
        line, = ax.plot(date, row, label=leg, marker='o')

        for x, y in zip(line.get_xdata(), line.get_ydata()):
            ax.annotate('{}'.format(y),
                            xy=(x, y),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

    ax.set_title(other_names[0])
    ax.set_xlabel(other_names[1])
    ax.set_ylabel(other_names[2])
    ax.set_xticklabels(date)
    ax.legend()
    try:
        plt.savefig('img/' + pict_name + '.png', bbox_inches='tight', dpi=80)
        return True
    except Exception as e:
        return False

