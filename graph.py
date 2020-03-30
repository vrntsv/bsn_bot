import numpy as np
import matplotlib.pyplot as plt


def bar_chart(data, date, legend, pict_name, other_names = ['' for i in range(3)]):
    # data - матрица, тип ndarray, число строк = длина legend, число столбцов = длина date
    # date - список со строками
    # legend - список со строками
    # pict_name - строка
    # other_names - список со строками [название графика, название оси x, название оси y]
    data = data.transpose()
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
    plt.savefig(pict_name + '.png', bbox_inchåes='tight', dpi=80)


def line_chart(data, date, legend, pict_name, other_names = ['' for i in range(3)]):
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
    plt.savefig(pict_name + '.png', bbox_inches='tight', dpi=80)


# data = np.array([[1, 20, 30],
#                  [40, 5, 6],
#                  [7, 80, 9]])

data = np.random.randint(500, size=(3, 30))
print(data)
legend = ['Alex', 'Boris', 'Gena']
# date = ['10.03.2020', '12.04.2020', '15.05.2021']
date = [f'{i}' for i in range(30)]
other_names = ['Название графика', 'Ось x', 'Ось y']

bar_chart(data, date, legend, 'name_bar', other_names)

line_chart(data, date, legend, 'name_line', other_names)