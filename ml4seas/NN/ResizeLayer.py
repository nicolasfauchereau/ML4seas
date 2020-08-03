import tensorflow as tf

class ResizeLayer(tf.keras.layers.Layer):     
    def __init__(self, newsize=None, **kwargs):
        super(ResizeLayer, self).__init__(**kwargs)
        self.resize_newsize = newsize     
    def call(self, input):
        return tf.image.resize(input, self.resize_newsize)
    def get_config(self):         
        return {'newsize': self.resize_newsize}