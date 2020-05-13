from keras.models import Sequential
from keras.layers import Dense, Activation, Conv1D, MaxPooling1D, Flatten


def train_model(trainX, trainY, testX, testY):
    model = Sequential([
            Conv1D(32, kernel_size=5, input_shape=(514, 12)),
            MaxPooling1D(),
            Activation('relu'),
            Conv1D(64, kernel_size=5),
            MaxPooling1D(),
            Activation('relu'),
            Conv1D(128, kernel_size=5),
            MaxPooling1D(),
            Activation('relu'),
            Flatten(),
            Dense(20),
            Activation('relu'),
            Dense(2),
            Activation('softmax')
        ])
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(trainX,
              trainY,
              epochs=10,
              batch_size=32,
              validation_data=(testX, testY))

    return model
