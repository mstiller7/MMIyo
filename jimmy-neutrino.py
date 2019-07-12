from numpy import amax, amin, array, dot, exp, random
from sklearn import preprocessing


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
    tsi = array([
        [22, 22, 25, 28, 67, 144, 53, 20],  # relaxed
        [20, 22, 24, 26, 61, 126, 53, 19],
        [21, 26, 25, 24, 54, 126, 53, 17],
        [18, 26, 26, 25, 54, 129, 47, 14],
        [16, 28, 28, 27, 50, 117, 37, 14],
        [17, 27, 28, 29, 50, 115, 29, 13],
        [16, 28, 28, 31, 62, 127, 27, 15],
        [17, 26, 26, 33, 62, 121, 34, 19],
        [21, 26, 26, 33, 62, 129, 38, 20],
        [26, 34, 27, 32, 64, 125, 41, 23],
        [27, 37, 27, 30, 67, 114, 41, 24],
        [28, 37, 34, 27, 55, 90, 41, 24],
        [26, 36, 40, 26, 59, 98, 37, 21],
        [24, 37, 45, 26, 58, 83, 32, 21],
        [21, 31, 43, 26, 55, 86, 31, 21],
        [22, 29, 44, 31, 50, 99, 35, 21],
        [21, 27, 38, 32, 50, 104, 37, 21],
        [22, 25, 33, 31, 49, 98, 34, 22],
        [21, 30, 26, 30, 48, 113, 34, 21],
        [21, 29, 27, 31, 59, 114, 36, 21],
        # [144, 170, 74, 66, 168, 526, 210, 61],  # point
        # [235, 179, 87, 73, 173, 562, 221, 70],
        # [236, 189, 99, 85, 180, 592, 223, 76],
        # [250, 221, 98, 84, 182, 590, 210, 73],
        # [277, 234, 99, 78, 135, 527, 190, 64],
        # [279, 213, 97, 77, 146, 596, 167, 62],
        # [222, 227, 89, 74, 153, 575, 173, 59],
        # [252, 270, 79, 71, 176, 615, 190, 72],
        # [250, 260, 75, 72, 188, 647, 190, 80],
        # [223, 251, 80, 76, 199, 661, 179, 82],
        # [234, 274, 77, 74, 189, 627, 191, 90],
        # [227, 261, 76, 70, 195, 630, 174, 86],
        # [260, 212, 80, 66, 179, 540, 166, 72],
        # [241, 193, 87, 71, 176, 518, 167, 63],
        # [247, 194, 79, 69, 164, 474, 172, 73],
        # [259, 178, 76, 66, 160, 410, 152, 62],
        # [255, 182, 74, 69, 147, 399, 164, 68],
        # [197, 182, 73, 66, 133, 433, 208, 73],
        # [227, 181, 68, 60, 132, 406, 225, 78],
        # [225, 204, 74, 63, 182, 549, 225, 73],
        [113, 176, 75, 89, 83, 382, 217, 90],  # clench
        [120, 171, 72, 81, 99, 440, 215, 94],
        [125, 175, 67, 85, 100, 460, 174, 105],
        [119, 136, 66, 88, 110, 493, 192, 104],
        [145, 142, 73, 101, 106, 434, 195, 126],
        [139, 139, 80, 103, 106, 453, 196, 135],
        [141, 143, 80, 98, 98, 376, 203, 137],
        [163, 149, 73, 100, 104, 407, 205, 131],
        [165, 150, 69, 97, 101, 370, 183, 122],
        [156, 174, 66, 97, 96, 349, 230, 116],
        [162, 191, 65, 89, 110, 399, 230, 118],
        [162, 199, 80, 95, 108, 434, 247, 115],
        [158, 218, 105, 104, 106, 444, 258, 118],
        [150, 219, 107, 104, 101, 481, 264, 111],
        [149, 192, 111, 104, 97, 489, 249, 89],
        [175, 176, 109, 116, 77, 417, 272, 91],
        [173, 198, 109, 115, 84, 420, 262, 94],
        [152, 180, 97, 101, 84, 381, 244, 89],
        [160, 180, 103, 108, 83, 358, 237, 95],
        [156, 187, 99, 95, 85, 377, 213, 109]
    ])
    tso = array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        #  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ]).T

    # Normalize the inputs.
    tsi = tsi.T # transpose to get an idea of the importance of each individual sensor.
    mms = preprocessing.MinMaxScaler()
    tsi = mms.fit_transform(tsi)
    tsi = tsi.T # flip it back to normal.

    # Train the neural network using a training set.
    # Do it 10,000 times and make small adjustments each time.
    neural_network.train(tsi, tso, 10000)

    print "New synaptic weights after training: "
    print neural_network.synaptic_weights

    # Test the neural network with a new situation.
    print "Considering new situation 'relaxed' -> ?: "
    print neural_network.think(
        array(
            [17, 19, 24, 24, 90, 120, 32, 21]))
    # print "Considering new situations 'point' -> ?"
    # print neural_network.think(
    #     array(
    #         [323, 228, 65, 59, 196, 632, 228, 94]))
    # print neural_network.think(
    #     array(
    #         [316, 254, 61, 51, 184, 629, 229, 90]))
    # print neural_network.think(
    #     array(
    #         [294, 254, 56, 50, 191, 623, 244, 85]))
    print "Considering new situation 'clench' -> ?: "
    print neural_network.think(
        array(
            [120, 150, 64, 84, 93, 363, 217, 84]))
