import mxnet as mx
from mxnet import nd, autograd, gluon
import matplotlib
import matplotlib.pyplot as pt

from loguru import logger

def logistic(x):
    return 1. / (1. + nd.exp(-x))

x = nd.arange(-5, 5, .1)
y = logistic(x)

pt.title("Sigmoid function curve")
pt.plot(x.asnumpy(), y.asnumpy())
pt.savefig("figures/sigmoid.png")

# for linux users with NVIDIA GPUs: nvidia-smi tells you which number each GPU is assigned
data_ctx = mx.gpu(0)
model_ctx = mx.gpu(0)

with open("data/adult/a1a.train") as f:
    train_raw = f.read()

with open("data/adult/a1a.test") as f:
    test_raw = f.read()

# data looks like this 
# -1 5:1 7:1 14:1 19:1 39:1 40:1 51:1 63:1 67:1 73:1 74:1 76:1 78:1 83:1 \n
# first entry is the label, followed byt he indixes of the non zero features
# the 1 doesnt mean anything

def process_data(raw_data):
    train_lines = raw_data.splitlines()
    num_examples = len(train_lines)
    num_features = 123
    X = nd.zeros((num_examples, num_features), ctx=data_ctx)
    Y = nd.zeros((num_examples, 1), ctx=data_ctx)
    for i, line in enumerate(train_lines):
        tokens = line.split()
        label = (int(tokens[0]) + 1) / 2 # change label from {-1, 1} to {0, 1}
        Y[i] = label
        for token in tokens[1:]:
            index = int(token[:-2]) - 1
            X[i, index] = 1
    return X, Y

logger.info("Processing data")
Xtrain, Ytrain = process_data(train_raw)
Xtest, Ytest = process_data(test_raw)

logger.info("Shapes of train and test data: X_train, Y_train, X_test, Y_test")
logger.info(Xtrain.shape)
logger.info(Ytrain.shape)
logger.info(Xtest.shape)
logger.info(Ytest.shape)

# fraction of pos to negative examples in the train and test datasets
logger.info("Fraction of pos to neg in Y_train, Y_test")
logger.info(nd.sum(Ytrain)/len(Ytrain))
logger.info(nd.sum(Ytest)/len(Ytest))

# Create a data loader

batch_size = 64

train_data = gluon.data.DataLoader(gluon.data.ArrayDataset(Xtrain, Ytrain),
                                    batch_size=batch_size, shuffle=True)

test_data = gluon.data.DataLoader(gluon.data.ArrayDataset(Xtest, Ytest), 
                                    batch_size=batch_size, shuffle=True)

# define the model

net = gluon.nn.Dense(1)
net.collect_params().initialize(mx.init.Normal(sigma=1.), ctx=model_ctx)

trainer = gluon.Trainer(net.collect_params(), 'sgd', {"learning_rate": 0.01})

# define our log loss

def log_loss(output, y):
    yhat = logistic(output)
    return -nd.nansum(y*nd.log(yhat) + (1-y)*nd.log(1-yhat))

epochs = 30
loss_sequence = []
num_examples = len(Xtrain)

for e in range(epochs):
    cumulative_loss = 0
    for i, (data, label) in enumerate(train_data):
        data = data.as_in_context(model_ctx)
        label = label.as_in_context(model_ctx)
        with autograd.record():
            output = net(data)
            loss = log_loss(output, label)
        loss.backward()
        trainer.step(batch_size)
        cumulative_loss += nd.sum(loss).asscalar()
    logger.info(f"Epoch {e}, loss: {cumulative_loss}")
    loss_sequence.append(cumulative_loss)


# visualize learning curve

fig, ax = pt.subplots(figsize=(8, 6))
ax.plot(loss_sequence)
ax.grid(True, which="both")
ax.set_xlabel("Epoch", fontsize=14)
ax.set_ylabel("Average Loss", fontsize=14)


# calculate accuracy

num_correct = 0.
num_total = len(Xtest)

for i, (data, label) in enumerate(test_data):
    data = data.as_in_context(model_ctx)
    label = label.as_in_context(model_ctx)
    output = net(data)
    prediction = (nd.sign(output) + 1) / 2
    num_correct += nd.sum(prediction == label)

accuracy = (num_correct.asscalar() / num_total)
logger.success(f"Accuracy: {accuracy}")

ax.text(-0.1, 1.07, f'Accuracy: {accuracy}', style='italic',
    bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10},
    transform=ax.transAxes)
ax.set_title("Loss and Accuracy")
pt.savefig("figures/loss_and_accuracy.png")