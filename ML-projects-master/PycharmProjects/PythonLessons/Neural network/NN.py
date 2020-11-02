from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
import numpy as np
import numpy.random as r
import mfcc
import matplotlib.pyplot as plt
import random


def take_part_of_array(IT, n, y):
    partIT = list()
    party = list()
    for i in range(n):
        k = random.randint(0, len(IT) - 1)
        partIT.append(IT[k])
        party.append(y[k])
    return partIT, party


def convert_y_to_vect(y):
    y_vect = np.zeros((len(y), 10))
    for i in range(len(y)):
        y_vect[i, y[i]] = 1
    return y_vect


########################################################################################################################
"""

def f(x):  #sigmoid
    return 1 / (1 + np.exp(-x))


def f_deriv(x):
    return f(x) * (1 - f(x))

"""


########################################################################################################################


def f(x):  # tangh
    return (np.exp(2 * x) - 1) / (np.exp(2 * x) + 1)


def f_deriv(x):
    return 1 - f(x) ** 2


########################################################################################################################


def setup_and_init_weights(nn_structure):
    W = {}
    b = {}
    for l in range(1, len(nn_structure)):
        W[l] = r.random_sample((nn_structure[l], nn_structure[l - 1]))
        b[l] = r.random_sample((nn_structure[l],))
    return W, b


def init_tri_values(nn_structure):
    tri_W = {}
    tri_b = {}
    for l in range(1, len(nn_structure)):
        tri_W[l] = np.zeros((nn_structure[l], nn_structure[l - 1]))
        tri_b[l] = np.zeros((nn_structure[l],))
    return tri_W, tri_b


def feed_forward(x, W, b):
    h = {1: x}
    z = {}
    for l in range(1, len(W) + 1):
        # if it is the first layer, then the input into the weights is x, otherwise,
        # it is the output from the last layer
        if l == 1:
            node_in = x
        else:
            node_in = h[l]
        z[l + 1] = W[l].dot(node_in) + b[l]  # z^(l+1) = W^(l)*h^(l) + b^(l)
        h[l + 1] = f(z[l + 1])  # h^(l) = f(z^(l))
    return h, z


def calculate_out_layer_delta(y, h_out, z_out):
    # delta^(nl) = -(y_i - h_i^(nl)) * f'(z_i^(nl))
    return -(y - h_out) * f_deriv(z_out)


def calculate_hidden_delta(delta_plus_1, w_l, z_l):
    # delta^(l) = (transpose(W^(l)) * delta^(l+1)) * f'(z^(l))
    return np.dot(np.transpose(w_l), delta_plus_1) * f_deriv(z_l)


def train_nn(nn_structure, X, y, W, b, iter_num=600, alpha=0.05):
    #print(len(W))
    if len(W) == 0:
        W, b = setup_and_init_weights(nn_structure)
    cnt = 0
    #  print("y -", len(y))
    m = len(y)
    avg_cost_func = []
    print('Starting gradient descent for {} iterations'.format(iter_num))
    while cnt < iter_num:
        # if cnt%100 == 0:
        # print('Iteration {} of {}'.format(cnt, iter_num))
        tri_W, tri_b = init_tri_values(nn_structure)
        avg_cost = 0
        for i in range(len(y)):
            delta = {}
            # perform the feed forward pass and return the stored h and z values, to be used in the
            # gradient descent step
            h, z = feed_forward(X[i, :], W, b)
            # loop from nl-1 to 1 backpropagating the errors
            for l in range(len(nn_structure), 0, -1):
                if l == len(nn_structure):
                    delta[l] = calculate_out_layer_delta(y[i, :], h[l], z[l])
                    avg_cost += np.linalg.norm((y[i, :] - h[l]))
                else:
                    if l > 1:
                        delta[l] = calculate_hidden_delta(delta[l + 1], W[l], z[l])
                    # triW^(l) = triW^(l) + delta^(l+1) * transpose(h^(l))
                    tri_W[l] += np.dot(delta[l + 1][:, np.newaxis], np.transpose(h[l][:, np.newaxis]))
                    # trib^(l) = trib^(l) + delta^(l+1)
                    tri_b[l] += delta[l + 1]
        # perform the gradient descent step for the weights in each layer
        for l in range(len(nn_structure) - 1, 0, -1):
            W[l] += -alpha * (1.0 / m * tri_W[l])
            b[l] += -alpha * (1.0 / m * tri_b[l])
        # complete the average cost calculation
        avg_cost = 1.0 / m * avg_cost
        avg_cost_func.append(avg_cost)
        cnt += 1
    return W, b, avg_cost_func


def predict_y(W, b, X, n_layers):
    m = X.shape[0]
    y = np.zeros((m,))
    for i in range(m):
        h, z = feed_forward(X[i, :], W, b)
        y[i] = np.argmax(h[n_layers])
    return y


if __name__ == "__main__":
    # for j in range(10):
        # print("=======================>", j)
        # load data and scale
        ytest = []
        ytrainR = []
        ytrainW = []
        ITR, yrainR = mfcc.get_features("./data/input_train_right/", ytrainR, [1])
        ITW, ytrainW = mfcc.get_features("./data/input_train_wrong/", ytrainW, [0])
        IOR, ytest = mfcc.get_features("./data/input_test_right/", ytest, [1])
        IOW, ytest = mfcc.get_features("./data/input_test_wrong/", ytest, [0])
        ITest = IOR + IOW
        ITest, ytest = shuffle(ITest, ytest)  # mixing
        ytest = np.asarray(ytest)  # lists to ndarrays
        ITest = np.asarray(ITest)

        nn_structure = [11, 15, 10]  # setup the NN structure
        W = list()
        b = list()

        for i in range(10):
            part_of_ITR, part_of_ytrainR = take_part_of_array(ITR, 200, ytrainR)
            part_of_ITW, part_of_ytrainW = take_part_of_array(ITW, 200, ytrainW)
            # part_of_ITR = np.random.choice(ITR, 300)
            # part_of_ITW = np.random.choice(ITW, 300)

            ITrain = part_of_ITR + part_of_ITW
            ytrain = part_of_ytrainR + part_of_ytrainW
            ITrain, ytrain = shuffle(ITrain, ytrain)  # mixing
            yvtrain = convert_y_to_vect(ytrain)  # convert digits to vectors
            yvtrain = np.asarray(yvtrain)  # lists to ndarrays
            ITrain = np.asarray(ITrain)
            W, b, avg_cost_func = train_nn(nn_structure, ITrain, yvtrain, W, b)  # train the NN

            # plot the avg_cost_func
            plt.plot(avg_cost_func)
            plt.ylabel('Average J')
            plt.xlabel('Iteration number')
            plt.show()

        # get the prediction accuracy and print
        y_pred = predict_y(W, b, ITest, 3)
        print(' - Prediction accuracy is {}%'.format(accuracy_score(ytest, y_pred) * 100))
        plt.show()