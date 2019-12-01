import pickle
import random
import time

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from nn.resnet import resnet
from nn.training_utils import sparse_game_to_numpy


def load_data():
    print("#" * 80)
    print("Loading data...")

    games_list = []
    for filename in FILE_LIST:
        print("Loading file: {}".format(filename))
        with open(filename, 'rb') as f:
            unpickled_list = pickle.load(f)
        games_list += unpickled_list

    print("Finished loading data.")

    return games_list


def preprocess_data():
    print("#" * 80)
    print("Pre-processing data...")
    random.shuffle(data)
    num_games = len(data)
    num_training = int(TRAINING_DATA_PERCENT / 100 * num_games)

    training_games = data[:num_training]
    test_games = data[num_training:]

    training_samples = []
    test_samples = []
    training_labels = []
    test_labels = []

    for game in training_games:
        samples, labels = sparse_game_to_numpy(game, START_AT_MOVE)
        training_samples += samples
        training_labels  += labels
    for game in test_games:
        samples, labels = sparse_game_to_numpy(game, START_AT_MOVE)
        test_samples += samples
        test_labels  += labels

    print("Finished pre-processing data.")

    return np.array(training_samples), np.array(test_samples), np.array(training_labels), np.array(test_labels)


def initialize_model():
    print("#" * 80)
    print("Initializing model...")

    resnet_model = resnet(input_shape=(8, 8, 13), classes=2)

    resnet_model.summary()

    print("Finished initializing model.")

    return resnet_model


def train_model():
    print("#" * 80)
    print("Training model...")

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH, verbose=1,
                                                     save_weights_only=True, period=1)

    model.save_weights(CHECKPOINT_PATH.format(epoch=0))
    t = time.time()
    training_hist = model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=1,
                              validation_data=(X_test, y_test), callbacks=[cp_callback])
    print('Training time: %s' % (time.time() - t))

    print("Finished training model.")

    model.save(SAVE_PATH)

    print("Saved model to '{}'.".format(SAVE_PATH))

    return training_hist


def show_training_stats():
    # visualizing losses and accuracy
    train_loss = hist.history['loss']
    val_loss = hist.history['val_loss']
    train_acc = hist.history['accuracy']
    val_acc = hist.history['val_accuracy']
    xc = range(EPOCHS)

    plt.figure(1, figsize=(7, 5))
    plt.plot(xc, train_loss)
    plt.plot(xc, val_loss)
    plt.xlabel('num of Epochs')
    plt.ylabel('loss')
    plt.title('train_loss vs val_loss')
    plt.grid(True)
    plt.legend(['train', 'val'])
    plt.style.use('classic')

    plt.figure(2, figsize=(7, 5))
    plt.plot(xc, train_acc)
    plt.plot(xc, val_acc)
    plt.xlabel('num of Epochs')
    plt.ylabel('accuracy')
    plt.title('train_acc vs val_acc')
    plt.grid(True)
    plt.legend(['train', 'val'], loc=4)
    plt.style.use('classic')


FILE_LIST = ["data/custom_format/KingBaseLite2019-A40-A79.pkl"]
TRAINING_DATA_PERCENT = 70
START_AT_MOVE = 20

BATCH_SIZE = 32
EPOCHS = 3

CHECKPOINT_PATH = "model/checkpoints/cp-{epoch:04d}.ckpt"
SAVE_PATH = "model/saved_model.h5"


if __name__ == "__main__":

    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data()
    model = initialize_model()
    hist = train_model()
    show_training_stats()
