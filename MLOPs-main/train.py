import csv
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Load the data from the CSV file
with open('creditcard.csv', mode='r') as file:
    reader = csv.reader(file)
    data = []
    for row in reader:
        data.append(row)

# Split the data into features and labels
features = []
labels = []
for row in data[1:]:
    features.append(row[:-1])
    labels.append(row[-1])

# Convert the features and labels to float and integer data types
for i in range(len(features)):
    for j in range(len(features[0])):
        features[i][j] = float(features[i][j])
    labels[i] = int(labels[i])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

# Train the decision tree classifier
clf = DecisionTreeClassifier(max_depth=10)
clf.fit(X_train, y_train)

# Predict the labels for the test set
y_pred = clf.predict(X_test)

# Print the accuracy of the classifier
accuracy = sum(1 for i in range(len(y_pred)) if y_pred[i] == y_test[i]) / float(len(y_pred))
# Now print to file
with open("metrics.json", 'w') as outfile:
        json.dump({ "accuracy": accuracy}, outfile)
