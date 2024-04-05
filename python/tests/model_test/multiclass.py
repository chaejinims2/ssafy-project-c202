import cv2
import numpy as np
import tensorflow as tf

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="selfie_multiclass_256x256.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Read the image and resize it to the model's input size
image = cv2.imread('input.jpg')
image = cv2.resize(image, (256, 256))
image = np.expand_dims(image, axis=0)

# Set the tensor to point to the input data to be inferred
interpreter.set_tensor(input_details[0]['index'], image)

# Run the inference
interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])

# Process the output data as needed
# ...