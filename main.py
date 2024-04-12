import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def create_arrays(original_array):
    picture_array_red = original_array[:, :, 0]
    picture_array_green = original_array[:, :, 1]
    picture_array_blue = original_array[:, :, 2]
    return picture_array_red, picture_array_green, picture_array_blue


def calculate_frequencies(arrays):
    frequencies = [{str(i): 0 for i in range(256)} for _ in range(3)]
    for array, frequency in zip(arrays, frequencies):
        for value in array.flatten():
            frequency[str(value)] += 1
    return frequencies


def plot_color_distributions(frequencies):
    colors = ["red", "green", "blue"]
    fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    for i, color in enumerate(colors):
        data = list(frequencies[i].keys())
        bars = list(frequencies[i].values())
        axs[i].bar(data, bars, color=color)
    plt.show()


def main():
    picture = Image.open("img/image_clear.jpeg")
    picture_array = np.array(picture.convert("RGB"))
    picture_array_red, picture_array_green, picture_array_blue = create_arrays(
        picture_array
    )

    arrays = [picture_array_red, picture_array_green, picture_array_blue]
    frequencies = calculate_frequencies(arrays)

    plot_color_distributions(frequencies)


if __name__ == "__main__":
    main()
