import tf_keras as keras  # Importando tf-keras – uma versão do Keras compatível com modelos .h5
from tf_keras.models import load_model  # Importando a função load_model do tf_keras, que permite abrir o modelo
from PIL import Image, ImageOps  # Instalando pillow no lugar do PIL
import numpy as np

def get_class(model, label, image, top_k=2):
  # Disable scientific notation for clarity
  np.set_printoptions(suppress=True)

  # Load the model
  model = load_model(model, compile=False)

  # Load the labels
  class_names = [line.strip() for line in open(label, "r", encoding="utf-8") if line.strip()]

  image = Image.open(image).convert("RGB")

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)[0]

  ranked = sorted(enumerate(prediction), key=lambda item: item[1], reverse=True)[:top_k]

  results = []
  for index, score in ranked:
    label_text = class_names[index] if index < len(class_names) else f'class_{index}'
    parts = label_text.split(maxsplit=1)
    if parts and parts[0].isdigit() and len(parts) > 1:
      label_text = parts[1]
    results.append((label_text, float(score)))

  return results