import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Flatten,Dropout

# model = Sequential([
#     hub.Module('')

# ])

model = tf.keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4",
                   trainable=True),
    Dropout(0.3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.build([None,224,224,3])
print(model.summary())