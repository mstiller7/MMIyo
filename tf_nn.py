# https://easy-tensorflow.com/tf-tutorials/neural-networks/two-layer-neural-network

import tensorflow as tf

import numpy as np
import matplotlib as mpl

rpc_in = np.array([
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
    [144, 170, 74, 66, 168, 526, 210, 61],  # point
    [235, 179, 87, 73, 173, 562, 221, 70],
    [236, 189, 99, 85, 180, 592, 223, 76],
    [250, 221, 98, 84, 182, 590, 210, 73],
    [277, 234, 99, 78, 135, 527, 190, 64],
    [279, 213, 97, 77, 146, 596, 167, 62],
    [222, 227, 89, 74, 153, 575, 173, 59],
    [252, 270, 79, 71, 176, 615, 190, 72],
    [250, 260, 75, 72, 188, 647, 190, 80],
    [223, 251, 80, 76, 199, 661, 179, 82],
    [234, 274, 77, 74, 189, 627, 191, 90],
    [227, 261, 76, 70, 195, 630, 174, 86],
    [260, 212, 80, 66, 179, 540, 166, 72],
    [241, 193, 87, 71, 176, 518, 167, 63],
    [247, 194, 79, 69, 164, 474, 172, 73],
    [259, 178, 76, 66, 160, 410, 152, 62],
    [255, 182, 74, 69, 147, 399, 164, 68],
    [197, 182, 73, 66, 133, 433, 208, 73],
    [227, 181, 68, 60, 132, 406, 225, 78],
    [225, 204, 74, 63, 182, 549, 225, 73],
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


def load_data(mode='train'):
    '''
    Supply data for training or testing.
    '''
    if mode == 'train':

    elif mode == 'test':

    return

x_train, y_train, x_valid, y_valid = load_data(mode='train')

def randomize(x, y):
    '''
    Randomize the order of data samples and their corresponding labels.
    '''
    p = np.random.permutation(y.shape[0])
    s_x = x[p, :]
    s_y = y[p]
    return s_x, s_y


def getNextBatch(x, y, start, end):
    x_batch = x[start:end]
    y_batch = y[start:end]
    return x_batch, y_batch

# Helper functions to create the network.


def varWeight(name, shape):
    '''
    Create a weight variable.
    '''
    i = tf.truncated_normal_initializer(stddev=0.01)
    return tf.get_variable('W_' + name,
                           dtype=tf.float32,
                           shape=shape,
                           initializer=i)


def varBias(name, shape):
    '''
    Create a bias variable.
    '''
    i = tf.constant(0., shape=shape, dtype=tf.float32)
    return tf.get_variable('b_' + name,
                           dtype=tf.float32,
                           initializer=i)


def fcLayer(x, name, n_units, use_relu=True):
    '''
    Create a fully-connected (dense) layer.
    x = input from the previous layer.
    '''
    dim = x.get_shape()[1]
    W = varWeight(name, shape=[dim, n_units])
    b = varBias(name, [n_units])
    layer = tf.matmul(x, W)
    layer += b
    if use_relu:
        layer = tf.nn.relu(layer)
    return layer


vector_l = 8
vector_h = 1
vector_flat = vector_l * vector_h
n_classes = 3  # relaxed, point, clench

nEpochs = 10
batchSize = 20
displayFreq = 100
learnRate = 0.001
h1_nodes = 200

# 4.1) Create placeholders for the inputs (x) and corresponding labels (y).
x = tf.placeholder(tf.float32, shape=[None, vector_flat], name='X')
y = tf.placeholder(tf.float32, shape=[None, n_classes], name='Y')

# 4.2) Create the network layers.
fc1 = fcLayer(x, h1_nodes, use_relu=True)
output_logits = fcLayer(fc1, n_classes, 'OUT', use_relu=False)

# 4.3) Define loss, optimizer, accuracy, and predicted class.
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    labels=y, logits=output_logits), name='loss')
optimizer = tf.train.AdamOptimizer(
    learning_rate=learnRate, name='Adam-op').minimize(loss)
correct_prediction = tf.equal(
    tf.argmax(output_logits, 1), tf.argmax(y, 1), name='correct_pred')
accuracy = tf.reduce_mean(
    tf.cast(correct_prediction, tf.float32), name='accuracy')

cls_prediction = tf.argmax(output_logits, axis=1, name='predictions')

# 4.4) Initialize all variables.
init = tf.global_variables_initializer()

# 5) Train.
sess = tf.InteractiveSession()
sess.run(init)

# number of training iterations in each epoch
n_iter = int(len(y_train) / batch_size)
for epoch in range(nEpochs):
    print('Training epoch: {}'.format(epoch + 1))
    # randomly shuffle the training data at the beginning of each epoch
    x_train, y_train = randomize(x_train, y_train)
    for i in range(n_iter):
        start = i * batchSize
        end = (i + 1) * batchSize
        x_batch, y_batch = getNextBatch(x_train, y_train, start, end)

        # run optimization operation ("back-propagation")
        feed_dict_batch = {x: x_batch, y: y_batch}
        sess.run(optimizer, feed_dict=feed_dict_batch)

        if i % display == 0:
            # calculate and display the batch loss and accuracy
            loss_batch, acc_batch = sess.run(
                [loss, accuracy], feed_dict=feed_dict_batch)
            print("iter {0:3d:\tLoss = {1:.2f},\tTraining Accuracy = {2:.01%").format(
                i, loss_batch, acc_batch)

    # run validation after every epoch
    feed_dict_valid = {x: x_valid[:1000], y: y_valid[:1000]}
    loss_valid, acc_valid = sess.run(
        [loss, accuracy], feed_dict=feed_dict_valid)
    print('---------------------------------------------------------')
    print("Epoch: {0}, validation loss: {1:.2f}, validation accuracy: {2:.01%}".
          format(epoch + 1, loss_valid, acc_valid))
    print('---------------------------------------------------------')
