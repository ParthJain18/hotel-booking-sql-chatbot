import matplotlib.pyplot as plt
import os
from langchain_core.tools import tool


@tool
def create_pie_chart(data: list[float], labels: list[str]) -> str:
    """
    Create a pie chart with the given data and labels and send it to the user as an image.

    Args:
    data (list[float]): The data to be displayed in the pie chart.
    labels (list[str]): The labels for the data.

    Returns:
    str: "success" if the image is created successfully.
    """
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    return _save_image_from_figure(fig)

@tool
def create_line_graph(x_data: list[float], y_data: list[float], title: str = '', xlabel: str = '', ylabel: str ='') -> str:
    """
    Create a line graph with the given data and labels and send it to the user as an image.

    Args:
    x_data (list[float]): The x-axis data.
    y_data (list[float]): The y-axis data.
    title (str): The title of the graph.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.

    Returns:
    str: "success" if the image is created successfully.
    """
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    return _save_image_from_figure(fig)

@tool
def create_bar_graph(x_data: list[float], y_data: list[float], title: str = '', xlabel:str ='', ylabel: str ='') -> str:
    """
    Create a bar graph with the given data and labels and send it to the user as an image.

    Args:
    x_data (list): The x-axis data.
    y_data (list): The y-axis data.
    title (str): The title of the graph.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.

    Returns:
    str: "success" if the image is created
    """
    fig, ax = plt.subplots()
    ax.bar(x_data, y_data)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    return _save_image_from_figure(fig)


def _save_image_from_figure(fig):
    os.makedirs('data/temp_figures', exist_ok=True)
    number = len(os.listdir('data/temp_figures'))
    fig.savefig(f'data/temp_figures/figure_{number}.png')
    plt.close(fig)
    return "Sucess"

graph_tools = [create_pie_chart, create_line_graph, create_bar_graph]

if __name__ == '__main__':
    pie_chart = create_pie_chart.invoke(input={"data":[10, 20, 30], "labels": ['A', 'B', 'C']})
    # line_graph = create_line_graph.invoke([1, 2, 3], [4, 5, 6], title='Line Graph', xlabel='X Axis', ylabel='Y Axis')
    # bar_graph = create_bar_graph.invoke(['A', 'B', 'C'], [10, 20, 30], title='Bar Graph', xlabel='Categories', ylabel='Values')
