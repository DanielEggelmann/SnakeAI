from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten
import snake
import numpy as np
from operator import itemgetter

def create_model(field_size):
    model = Sequential()
    #model.add(Conv1D(5, kernel_size=3, input_shape=field_size, activation="relu"))
    #model.add(Flatten())
    model.add(Dense(30, input_shape=field_size, activation="sigmoid"))
    model.add(Flatten())
    model.add(Dense(36, activation="sigmoid"))
    model.add(Dense(3, activation="softmax"))
    model.compile(optimizer="adam", loss="categorical_crossentropy")
    return model

def get_command(model, field):
    field = np.expand_dims(field, 0)
    result = model.predict(field)
    max = np.argmax(result)
    if max == 0:
        return snake.COMMAND_STRAIGHT
    elif max == 1:
        return snake.COMMAND_LEFT
    elif max == 2:
        return snake.COMMAND_RIGHT

def evaluate_entity(game):
    return game.score * len(game.used_fields) + len(game.used_fields)

#get number strongest individuals of the generation
def get_best(generation, number):
    scores = []
    for member in generation: #calculate scores
        scores.append((evaluate_entity(member[1]), member))
    return sorted(scores, key=itemgetter(0))[:number]

def mutate_model(model, max_mutation):
    for layer in model.layers:
        weights = layer.get_weights()
        for i in range(len(weights)):
            weights[i] = weights[i] + (2 * np.random.random_sample(weights[i].shape) - 1) * max_mutation
        layer.set_weights(weights)
    return model

def backpropagate_scores(model, scores):
    pass
#w[:, 1:2] = w[:, 1:2] + x

if __name__ == "__main__":
    model = create_model((30, 30))

    #model.summary()
    for layer in model.layers:
        for w in layer.get_weights():
            print(w.shape)