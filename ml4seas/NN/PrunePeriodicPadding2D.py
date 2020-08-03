import tensorflow as tf

class PrunePeriodicPadding2D(tf.keras.layers.Layer):
    def __init__(self, pad_width, **kwargs):
        super().__init__(**kwargs)
        self.pad_width = pad_width

    def call(self, inputs, **kwargs):
        if self.pad_width == 0:
            return inputs
        inputs_pruned = inputs[:, self.pad_width:-self.pad_width, self.pad_width:-self.pad_width, :]
        return inputs_pruned

    def get_config(self):
        config = super().get_config()
        config.update({'pad_width': self.pad_width})
        return config