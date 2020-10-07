import mxnet as mx
from mxnet import nd, autograd, gluon

from loguru import logger
import matplotlib.pyplot as pt
mx.random.seed(42)

# Specify the mxnet context we are running on, CPU or GPU
data_ctx = mx.cpu()
model_ctx = mx.cpu()

"""
Linear Regression:
y is a linear combination of the features in input x plus a bias term

yhat = w1x1 + w2x2 + ... + b
yhat = dot(X, w) + b   

We will use mean squared error as a loss function
l(y, yhat) = sum((yhat_i - y_i) ^ 2) for all i within n predictions

"""

num_features = 2        # dimensionality of the input features
num_outputs = 1         # dimensionality of the labels
num_examples = 10000    # number of samples in the generated dataset

# Lets generate a fake dataset
def f(X):
    """
    'Ground Truth' function for our linear regression to predict
    X: a 2d input of shape (num_examples, num_features)
    returns: 1d f(X) as defined below
    """

    return 3 * X[:, 0] - 5 * X[:, 1] + 2

logger.info("Generating data")
X = nd.random_normal(shape=(num_examples, num_features), ctx=data_ctx)
noise = 0.1 * nd.random_normal(shape=(num_examples,), ctx=data_ctx)
y = f(X) + noise

logger.info(f"Sample input X: {X[0]}")
logger.info(f"Sample output y: {y[0]}")

# Plot the data 
fig, (ax1, ax2) = pt.subplots(1, 2)
ax1.set_title(f"feature 0, y")
ax1.scatter(X[:, 0].asnumpy(), y.asnumpy(), facecolor='orange')
ax2.set_title(f"feature 1, y")
ax2.scatter(X[:, 1].asnumpy(), y.asnumpy(), facecolor='green')
pt.savefig("figures/feature_correspondence.png")

# ArrayDataset allows us to iterate quickly through our dataset 
# DataLoader allows us to easily grab random bactches of data
logger.info("Creating training set")
batch_size = 10
train_data = gluon.data.DataLoader(gluon.data.ArrayDataset(X, y),
                                    batch_size=batch_size, shuffle=True)

# Note: we can actually grab batches of data by iterating normally

logger.info(f"Num batches: {len(train_data)}")

# Time to start building the model

# Allocate initial parameters
w = nd.random_normal(shape=(num_features, num_outputs), ctx=model_ctx)
b = nd.random_normal(shape=num_outputs, ctx=model_ctx)
params = [w, b]

# Allocate memory for parameter gradient
for param in params:
    param.attach_grad()

# Define our model, basically the simplest possible useful neural network
# Two layers, input layer of (num_features) nodes, and an output layer of (num_outputs) nodes 
# with the identity function as the activation function
def net(X):
    return nd.dot(X, w) + b

# Define our loss function as the mean squared error
def square_loss(yhat, y):
    return nd.mean((yhat-y) ** 2)

# Define our optimizer, in this case we will be using mini batch gradient descent
# At each update step we will calculate the gradient of the loss function with respect to our weights
# using a randomly selected batch of data points
def MBGD(params, lr):
    for param in params:
        param[:] = param - lr*param.grad        # Note, param[:] signifies an inplace operation. A temporary buffer is still created. This can be removed by calling the root mxnet funciton, but it's not necesarry here

def plot(X, losses, figpath, sample_size=100):
    x = list(range(len(losses)))
    fig, (ax1, ax2, ax3) = pt.subplots(1, 3, figsize=(20,10))
    pt.subplots_adjust(hspace=0.3)
    ax1.set_title("Loss during training")
    ax1.plot(x, losses, '-r')
    ax2.set_title("Estimated v Real function | feature 0")
    ax2.plot(X[:sample_size, 0].asnumpy(), 
                net(X[:sample_size, :]).asnumpy(), 'or', label="Estimated")
    ax2.plot(X[:sample_size, 0].asnumpy(),
                f(X[:sample_size, :]).asnumpy(), '*g', label="Real")
    ax2.legend()
    ax3.set_title("Estimated v Real function feature 1")
    ax3.plot(X[:sample_size, 1].asnumpy(), 
                net(X[:sample_size, :]).asnumpy(), 'or', label="Estimated")
    ax3.plot(X[:sample_size, 1].asnumpy(),
                f(X[:sample_size, :]).asnumpy(), '*g', label="Real")
    ax3.legend()

    pt.savefig(figpath)

# Now we have to define the training loop
# For each pass (epoch) we will iterate through train_data, randomly grabbing batches
# For each batch we will:
    # Generate predictions yhat and loss loss by executing a forward pass through the network
    # Calcualte gradients by making a backwards pass through the network (loss.backward()) (hashtag chain rule)
    # Update our model parameters by invoking the MBGD optimizer
epochs = 10
losses = []
learning_rate = 1e-4
num_batches = len(train_data)

logger.info('Plotting initial predictions')
plot(X, losses, "figures/pre_training.png")

logger.info("Intiating training loop")
for epoch in range(epochs):
    cumulative_loss = 0

    for (data, label) in train_data:
        data = data.as_in_context(model_ctx)                        # https://mxnet.apache.org/versions/1.6/api/python/docs/tutorials/packages/ndarray/03-ndarray-contexts.html
        label = label.as_in_context(model_ctx).reshape((-1,1))      # This avoids accidentally re-copying data to a context (device) that it is already loaded into
        with autograd.record():
            yhat = net(data)
            loss = square_loss(yhat, label)
        loss.backward()
        MBGD(params, learning_rate)
        cumulative_loss += loss.asscalar()
    epoch_loss = cumulative_loss / num_batches
    losses.append(epoch_loss)
    logger.info(f" Epoch: {epoch+1}, Loss: {epoch_loss}")

logger.success("Training Completed")
logger.info("Plotting results")
plot(X, losses,"figures/post_training.png")
logger.success("Complete")
