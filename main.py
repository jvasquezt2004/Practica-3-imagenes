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


def make_equalization(image_array):
    output_image = np.zeros_like(image_array)
    for channel in range(3):
        channel_data = image_array[:, :, channel]
        histogram = np.zeros(256, dtype=int)
        for i in range(256):
            histogram[i] = np.sum(channel_data == i)
        cdf = histogram.cumsum()
        cdf_normalized = cdf * 255 / cdf[-1]
        equalized_data = cdf_normalized[channel_data.flatten()].astype(np.uint8)
        output_image[:, :, channel] = equalized_data.reshape(channel_data.shape)
    return output_image


def apply_operation(image_array, operation, value=1.0):
    if operation == "sumar":
        modified_array = np.clip(image_array + value, 0, 255)
    elif operation == "restar":
        modified_array = np.clip(image_array - value, 0, 255)
    elif operation == "multiplicar":
        modified_array = np.clip(image_array * value, 0, 255)
    elif operation == "dividir":
        modified_array = np.clip(image_array / value, 0, 255)
    elif operation == "gamma":
        gamma_corrected = np.array(255 * (image_array / 255) ** value, dtype="uint8")
        modified_array = gamma_corrected
    elif operation == "inversa":
        modified_array = 255 - image_array
    elif operation == "ecualizacion":
        modified_array = make_equalization(image_array)
    else:
        return image_array
    return modified_array.astype(np.uint8)


def main():
    picture = Image.open("img/image_clear.jpeg")
    operation = input(
        "Que operacion desea realizar? (sunmar, restar, multiplicar, dividir, gamma, inversa, ecualizacion): "
    )
    value = 1.0
    if operation in ["sunmar", "restar", "multiplicar", "dividir", "gamma", "inversa"]:
        value = float(input("Ingrese el valor para la operacion: "))

    picture_array = np.array(picture.convert("RGB"))
    modified_array = apply_operation(picture_array, operation, value)

    arrays = create_arrays(modified_array)
    frequencies = calculate_frequencies(arrays)

    plot_color_distributions(frequencies)

    modified_image = Image.fromarray(modified_array)
    modified_image.show()


if __name__ == "__main__":
    main()
