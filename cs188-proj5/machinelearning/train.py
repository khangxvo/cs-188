from torch import no_grad
from torch.utils.data import DataLoader


"""
Functions you should use.
Please avoid importing any other functions or modules.
Your code will not pass if the gradescope autograder detects any changed imports
"""
from torch import optim, tensor
from losses import regression_loss, digitclassifier_loss, languageid_loss, digitconvolution_Loss
from torch import movedim


"""
##################
### QUESTION 1 ###
##################
"""


def train_perceptron(model, dataset):
    """
    Train the perceptron until convergence.
    You can iterate through DataLoader in order to 
    retrieve all the batches you need to train on.

    Each sample in the dataloader is in the form {'x': features, 'label': label} where label
    is the item we need to predict based off of its features.
    """
    with no_grad():
        dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
        "*** YOUR CODE HERE ***"

        # keep track of convergence
        converged = False
        while not converged:
            converged = True # assume already converge

            # get every feature and label in the dataloader
            for batch in dataloader:
                x, label = batch['x'], batch['label']

                # calculate the prediction
                prediction = model.get_prediction(x)

                # if the prediction does not match the label, update the weight
                if prediction != label:
                    converged = False
                    model.w += label * x


def train_regression(model, dataset):
    """
    Trains the model.

    In order to create batches, create a DataLoader object and pass in `dataset` as well as your required 
    batch size. You can look at PerceptronModel as a guideline for how you should implement the DataLoader

    Each sample in the dataloader object will be in the form {'x': features, 'label': label} where label
    is the item we need to predict based off of its features.

    Inputs:
        model: Pytorch model to use
        dataset: a PyTorch dataset object containing data to be trained on
        
    """
    "*** YOUR CODE HERE ***"
    # hyperparameters
    learning_rate = 0.001
    batch_size = 32
    epochs = 1000
    target_loss = 0.01

    # create DataLoader
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle = True)

    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training Loop
    for epoch in range(epochs):
        epoch_loss = 0.0
        num_batches = 0

        for batch in dataloader:
            # get batch data
            x=batch['x']
            label = batch['label']

            # reset gradients
            optimizer.zero_grad()

            # forward pass and calculate loss
            y_pred = model(x)
            loss = regression_loss(y_pred, label)

            # calculate gradients
            loss.backward()

            # update weights
            optimizer.step()

            # track loss
            epoch_loss += loss.item()
            num_batches += 1

        # calculate average epoch loss
        avg_loss = epoch_loss / num_batches

        if avg_loss <= target_loss:
            break


def train_digitclassifier(model, dataset):
    """
    Trains the model.
    """
    model.train()
    """ YOUR CODE HERE """

    # hyperparameters
    learning_rate = 0.001
    batch_size = 32
    epochs = 1000
    target = 0.98

    # create data loader
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # create optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # training loop
    for _ in range(epochs):

        for batch in dataloader:
            # get the feature and true label
            x = batch['x']
            label = batch['label']

            # reset gradient
            optimizer.zero_grad()

            # foward
            y_pred = model(x)
            accurary = digitclassifier_loss(y_pred, label)

            # calculate gradient
            accurary.backward()

            # update weight
            optimizer.step()

        # if get the accuracy at least the target, break out early
        if dataset.get_validation_accuracy() >= target:
            break





def train_languageid(model, dataset):
    """
    Trains the model.

    Note that when you iterate through dataloader, each batch will returned as its own vector in the form
    (batch_size x length of word x self.num_chars). However, in order to run multiple samples at the same time,
    get_loss() and run() expect each batch to be in the form (length of word x batch_size x self.num_chars), meaning
    that you need to switch the first two dimensions of every batch. This can be done with the movedim() function 
    as follows:

    movedim(input_vector, initial_dimension_position, final_dimension_position)

    For more information, look at the pytorch documentation of torch.movedim()
    """
    model.train()
    "*** YOUR CODE HERE ***"

    # hyperparameters
    learning_rate = 0.001
    batch_size = 32
    epochs = 1000
    target = 0.815

    # create DataLoader
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle = True)

    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for _ in range(epochs):

        for batch in dataloader:
            # get the feature and true label
            x = movedim(batch['x'], 0, 1)
            label = batch['label']

            # reset gradient
            optimizer.zero_grad()

            # foward
            y_pred = model(x)
            accurary = languageid_loss(y_pred, label)

            # calculate gradient
            accurary.backward()

            # update weight
            optimizer.step()

        # if get the accuracy at least the target, break out early
        if dataset.get_validation_accuracy() > target:
            break
        



def Train_DigitConvolution(model, dataset):
    """
    Trains the model.
    """
    """ YOUR CODE HERE """

    # hyperparameters
    learning_rate = 0.001
    batch_size = 32
    epochs = 1000
    target = 0.81

    # create DataLoader
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle = True)

    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for _ in range(epochs):

        for batch in dataloader:
            # get the feature and true label
            x = batch['x']
            label = batch['label']

            # reset gradient
            optimizer.zero_grad()

            # foward
            y_pred = model(x)
            accurary = digitconvolution_Loss(y_pred, label)

            # calculate gradient
            accurary.backward()

            # update weight
            optimizer.step()

        # if get the accuracy at least the target, break out early
        if dataset.get_validation_accuracy() > target:
            break
