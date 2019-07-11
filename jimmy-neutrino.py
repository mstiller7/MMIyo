from numpy import exp, array, random, dot


class NeuralNetwork():
    def __init__(self):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.
        random.seed(1)

        # We model a single neuron, with 3 input connections and 1 output connection.
        # We assign random weights to a 3 x 1 matrix, with values in the range -1 to 1
        # and mean 0.
        self.synaptic_weights = 2 * random.random((8, 1)) - 1

    # The Sigmoid function, which describes an S shaped curve.
    # We pass the weighted sum of the inputs through this function to
    # normalise them between 0 and 1.
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    # It indicates how confident we are about the existing weight.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # We train the neural network through a process of trial and error.
    # Adjusting the synaptic weights each time.
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in xrange(number_of_training_iterations):
            # Pass the training set through our neural network (a single neuron).
            output = self.think(training_set_inputs)

            # Calculate the error (The difference between the desired output
            # and the predicted output).
            error = training_set_outputs - output

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            adjustment = dot(training_set_inputs.T, error *
                             self.__sigmoid_derivative(output))

            # Adjust the weights.
            self.synaptic_weights += adjustment

    # The neural network thinks.
    def think(self, inputs):
        # Pass inputs through our neural network (our single neuron).
        return self.__sigmoid(dot(inputs, self.synaptic_weights))


if __name__ == "__main__":

    # Intialise a single neuron neural network.
    neural_network = NeuralNetwork()

    print "Random starting synaptic weights: "
    print neural_network.synaptic_weights

    # The training set. We have 4 examples, each consisting of 3 input values
    # and 1 output value.
    training_set_inputs = array([
        [131, 153, 66, 106, 92, 355, 214, 102],  # clench
        [155, 177, 82, 115, 92, 346, 189, 104],
        [154, 190, 83, 117, 91, 355, 163, 102],
        [146, 183, 79, 109, 90, 365, 157, 97],
        [150, 181, 77, 102, 83, 307, 163, 89],
        [149, 191, 88, 100, 79, 272, 203, 86],
        [121, 178, 88, 118, 75, 277, 205, 75],
        [112, 158, 83, 117, 71, 287, 212, 71],
        [494, 257, 63, 53, 135, 340, 119, 55],  # point
        [504, 286, 60, 48, 129, 398, 127, 54],
        [434, 279, 61, 49, 135, 361, 126, 42],
        [419, 192, 58, 50, 168, 372, 128, 42],
        [385, 199, 60, 54, 174, 415, 132, 48],
        [371, 229, 58, 61, 177, 492, 140, 53],
        [352, 186, 63, 65, 181, 464, 156, 55],
        [384, 192, 63, 65, 176, 467, 177, 61]
    ])
    training_set_outputs = array([
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    ]).T

    # Train the neural network using a training set.
    # Do it 10,000 times and make small adjustments each time.
    neural_network.train(training_set_inputs, training_set_outputs, 10000)

    print "New synaptic weights after training: "
    print neural_network.synaptic_weights

    # Test the neural network with a new situation.
    print "Considering new situation 'clench' -> ?: "
    print neural_network.think(
        array([[94, 189, 75, 107, 88, 282, 224, 95]]))
    print "Considering new situation 'point' -> ?"
    print neural_network.think(
        array([[423, 157, 85, 63, 160, 484, 226, 67]]))
