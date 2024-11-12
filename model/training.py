import numpy as np
import json

# Define the SimpleLogisticModel class
class SimpleLogisticModel:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def train(self, X, y):
        samples, features = X.shape
        self.weights = np.zeros(features)
        self.bias = 0

        # Gradient Descent
        for _ in range(self.epochs):
            model = np.dot(X, self.weights) + self.bias
            predictions = self._sigmoid(model)

            # Compute gradients
            dw = (1 / samples) * np.dot(X.T, (predictions - y))
            db = (1 / samples) * np.sum(predictions - y)

            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        model = np.dot(X, self.weights) + self.bias
        predictions = self._sigmoid(model)
        return [1 if i > 0.5 else 0 for i in predictions]

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

# Training the model
np.random.seed(0)
data = np.random.randint(1, 10, (100, 5))  # Sample features
labels = (data[:, 1] > 5).astype(int)      # Sample labels based on a condition

model = SimpleLogisticModel()
model.train(data, labels)

# Save the model parameters as JSON
model_params = {
    "weights": model.weights.tolist(),
    "bias": model.bias
}

with open("model/cat_dog_model_params.json", "w") as f:
    json.dump(model_params, f)

print("Model parameters saved as a JSON file.")
