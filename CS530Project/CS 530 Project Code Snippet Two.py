"""A small binary classifier implemented with basic Python operations.

Assumptions:
    * Each dataset row is a tuple: (list of numeric features, integer label).
    * Labels are binary: 0 or 1.
    * All rows have the same number of features.
    * Training uses gradient descent for sigmoid and the perceptron update for
      step activation. Both training methods return (weights, bias).
"""


def _validate_activation(activation_function):
    if activation_function not in ("sigmoid", "step"):
        raise ValueError("activation_function must be 'sigmoid' or 'step'")


def _sigmoid(value):
    """Return a numerically stable sigmoid value."""
    if value >= 0:
        return 1.0 / (1.0 + pow(2.718281828459045, -value))
    exponential = pow(2.718281828459045, value)
    return exponential / (1.0 + exponential)


def single_neuron(inputs, weights, bias, activation_function):
    """Calculate one neuron's activated weighted sum."""
    _validate_activation(activation_function)
    if len(inputs) != len(weights):
        raise ValueError("inputs and weights must have the same length")

    weighted_sum = sum(input_value * weight for input_value, weight in zip(inputs, weights))
    weighted_sum += bias
    if activation_function == "sigmoid":
        return _sigmoid(weighted_sum)
    return 1 if weighted_sum >= 0 else 0


def binary_classifier(dataset, weights, bias, activation_function):
    """Return one binary prediction for each row in dataset."""
    _validate_activation(activation_function)
    return [
        single_neuron(features, weights, bias, activation_function)
        for features, _ in dataset
    ]


def create_synthetic_dataset():
    """Create a linearly separable two-feature OR dataset."""
    return [
        ([0.0, 0.0], 0),
        ([0.0, 1.0], 1),
        ([1.0, 0.0], 1),
        ([1.0, 1.0], 1),
    ]


def train_weights(dataset, activation_function, learning_rate=0.1, epochs=1000):
    """Train and return (weights, bias) for the supplied binary dataset."""
    _validate_activation(activation_function)
    if not dataset:
        raise ValueError("dataset must not be empty")
    if learning_rate <= 0 or epochs <= 0:
        raise ValueError("learning_rate and epochs must be positive")

    feature_count = len(dataset[0][0])
    weights = [0.0] * feature_count
    bias = 0.0

    for _ in range(epochs):
        for features, expected_label in dataset:
            if len(features) != feature_count or expected_label not in (0, 1):
                raise ValueError("dataset rows must have consistent features and 0/1 labels")

            prediction = single_neuron(features, weights, bias, activation_function)
            error = expected_label - prediction
            if activation_function == "sigmoid":
                error *= prediction * (1.0 - prediction)
            for index, feature in enumerate(features):
                weights[index] += learning_rate * error * feature
            bias += learning_rate * error

    return weights, bias


if __name__ == "__main__":
    dataset = create_synthetic_dataset()
    for activation in ("step", "sigmoid"):
        weights, bias = train_weights(dataset, activation)
        predictions = binary_classifier(dataset, weights, bias, activation)
        print(activation + " weights:", weights)
        print(activation + " bias:", bias)
        print(activation + " predictions:", predictions)