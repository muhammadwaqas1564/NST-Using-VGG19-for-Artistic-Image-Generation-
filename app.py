import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('style_transfer_model.h5')

# Preprocess the input images
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.vgg19.preprocess_input(img)
    return img

# Deprocess the output image for display
def deprocess_image(image):
    img = image.reshape((224, 224, 3))
    img[:, :, 0] += 103.939
    img[:, :, 1] += 116.779
    img[:, :, 2] += 123.68
    img = img[:, :, ::-1]
    img = np.clip(img, 0, 255).astype('uint8')
    return img

# Your existing style transfer code function
def fine_tune_style_transfer(content_image_path, style_image_path):
    # Load and preprocess images
    content_image = preprocess_image(content_image_path)
    style_image = preprocess_image(style_image_path)

    # Fine-tuning logic here (similar to your existing code)
    # This function should return the final stylized image
    # For the purpose of this demo, let's assume it's returned correctly.
    
    # Initialize generated image
    generated_image = tf.Variable(preprocess_image(content_image_path) * 0.6 + preprocess_image(style_image_path) * 0.4)
    # Perform the style transfer process here...
    # (Include your actual style transfer implementation here)

    final_image = deprocess_image(generated_image.numpy())
    return final_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'content_image' not in request.files or 'style_image' not in request.files:
        return redirect(request.url)

    content_image = request.files['content_image']
    style_image = request.files['style_image']

    if content_image.filename == '' or style_image.filename == '':
        return redirect(request.url)

    content_image_path = os.path.join('static/uploads', content_image.filename)
    style_image_path = os.path.join('static/uploads', style_image.filename)

    content_image.save(content_image_path)
    style_image.save(style_image_path)

    final_image = fine_tune_style_transfer(content_image_path, style_image_path)
    
    final_image_path = os.path.join('static/uploads', 'stylized_image.jpg')
    plt.imsave(final_image_path, final_image)

    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
