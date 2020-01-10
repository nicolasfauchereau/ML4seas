# https://gist.github.com/shadiakiki1986/2c293e364563492c65bffdb6122b4e92
from sklearn.preprocessing import MinMaxScaler #  normalize,
min_max_scaler = MinMaxScaler()
# def myNorm3(X): return normalize(X, norm='l2', axis=0)
def myNorm3(X): return min_max_scaler.fit_transform(X)

##########################################
import numpy as np
from matplotlib import pyplot as plt
def myPlot(X):
    X_plt = X+5*np.arange(X.shape[1])
    N_PLOT=200
    plt.plot(X_plt[0:N_PLOT,:])
    plt.show()

##############################################
# could make wrapper from https://gist.github.com/ktrnka/81c8a7b79cb05c577aab
# and make pipeline
# copied from simple example at https://blog.keras.io/building-autoencoders-in-keras.html
# from keras.layers import Input, Dense, Dropout
# from keras.models import Model, load_model
# from keras.layers.advanced_activations import LeakyReLU #, PReLU

from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import LeakyReLU

# new imports from tensorflow.keras added by Nicolas Fauchereau (Nicolas.Fauchereau@gmail.com) on 10/01/2020

def buildNetwork(input_shape:int, encoding_dim_ae:int=2):
    input_img = Input(shape=(input_shape,))
    encoded = input_img
    # encoded = Dense( encoding_dim_ae, activation='relu' )(encoded)

    # hidden layer
    encoded = Dense( encoding_dim_ae, activation='linear' )(encoded)

    # use leaky relu
    # https://github.com/fchollet/keras/issues/117
    encoded = LeakyReLU(alpha=.3)(encoded)   # add an advanced activation

    # GET DEEP
    # encoding_dim2 = 50
    # encoding_dim3 = 10
    # encoded = Dense(encoding_dim2, activation='relu')(encoded)
    # encoded = Dense(encoding_dim3, activation='relu')(encoded)
    # decoded = Dense(encoding_dim2, activation='relu')(encoded)

    decoded = Dense(input_shape, activation='sigmoid')(encoded)

    autoencoder = Model(input_img, decoded)
    encoder = Model(input_img, encoded)

    # encoded_input = Input(shape=(encoding_dim_ae,))
    # decoder_layer = autoencoder.layers[-1]
    # decoder = Model(encoded_input, decoder_layer(encoded_input))

    # other: optimizer='adadelta', loss='binary_crossentropy'
    autoencoder.compile(optimizer='rmsprop', loss='mean_squared_error')
    encoder.compile(optimizer='rmsprop', loss='mean_squared_error')
    # decoder.compile(optimizer='rmsprop', loss='mean_squared_error')
    
    return (autoencoder, encoder)

def buildNetwork2_deep(input_shape:int, enc_dim1:int, enc_dim2:int=None, enc_dim3:int=None, enc_dim4:int=None):
    if enc_dim2 is None and (enc_dim3 is not None or enc_dim4 is not None):
      raise Exception("dim2 is None but dim3 or dim4 is not None")
    if enc_dim3 is None and enc_dim4 is not None:
      raise Exception("dim3 is None but dim4 is not None")

    input_img = Input(shape=(input_shape,))
    encoded = input_img
    # encoded = Dense( encoding_dim_ae, activation='relu' )(encoded)

    # hidden layer
    encoded = Dense( enc_dim1, activation='linear' )(encoded)

    # use leaky relu
    # https://github.com/fchollet/keras/issues/117
    encoded = LeakyReLU(alpha=.3)(encoded)   # add an advanced activation

    # GET DEEP
    if enc_dim2 is not None:
      encoded = Dense(enc_dim2, activation='linear')(encoded)
      encoded = LeakyReLU(alpha=.3)(encoded)
      if enc_dim3 is not None:
        encoded = Dense(enc_dim3, activation='linear')(encoded)
        encoded = LeakyReLU(alpha=.3)(encoded)
        if enc_dim4 is not None:
          encoded = Dense(enc_dim4, activation='linear')(encoded)
          encoded = LeakyReLU(alpha=.3)(encoded)
          decoded = Dense(enc_dim3, activation='relu')(encoded)
        decoded = Dense(enc_dim2, activation='relu')(encoded)
      decoded = Dense(enc_dim1, activation='relu')(encoded)
    decoded = Dense(input_shape, activation='sigmoid')(encoded)

    autoencoder = Model(input_img, decoded)
    encoder = Model(input_img, encoded)

    # encoded_input = Input(shape=(encoding_dim_ae,))
    # decoder_layer = autoencoder.layers[-1]
    # decoder = Model(encoded_input, decoder_layer(encoded_input))

    # other: optimizer='adadelta', loss='binary_crossentropy'
    autoencoder.compile(optimizer='rmsprop', loss='mean_squared_error')
    encoder.compile(optimizer='rmsprop', loss='mean_squared_error')
    # decoder.compile(optimizer='rmsprop', loss='mean_squared_error')
    
    return (autoencoder, encoder)

from sklearn.model_selection import train_test_split
def ae_fit_encode_plot_mse(X_in, autoencoder, encoder, N_epochs, verbose=1):
  # split
  X_train, X_test = train_test_split(X_in, train_size=0.8, random_state=8888)

  # train autoencoder
  autoencoder.fit(
    X_train,
    X_train,
    epochs=N_epochs,
    batch_size=256,
    shuffle=True,
    validation_data=(
      X_test,
      X_test,
    ),
    verbose = verbose
  )

  # if not easy to visualize
  if X_in.shape[1]<50:
    # print("encoder predict")
    X_enc = encoder.predict(X_in)
    # print("encoded",X_enc)
    # # X_enc_dec = decoder.predict(X_enc)
    # # print("enc-dec",X_enc_dec)
    # X_rec = autoencoder.predict(X_pca)
    # print("recoded",X_rec)

    # plot
    # from matplotlib import pyplot as plt
    myPlot(X_enc)

  X_rec = autoencoder.predict(X_in)

  #result = mse(X_in, X_rec)
  #print("AE mse = ", result)
  #return result
  return X_rec

#####################
# functions for t1e_pca_ae_nonlinear-2
# copied from https://stats.stackexchange.com/questions/190148/autoencoder-pca-tensorflow?rq=1
def mse(x, x_est):
    return np.linalg.norm(x - x_est)/np.linalg.norm(x)

from sklearn.linear_model import LinearRegression
def pca_err(X, x_pca):
    #from sklearn.decomposition import PCA
    #pca = PCA(n_components=2).fit(X)
    #x_pca = pca.transform(X)
    lr = LinearRegression().fit(x_pca, X)
    x_est = lr.predict(x_pca)
    result = mse(X, x_est)
    print('err pca = ', result)
    return result
