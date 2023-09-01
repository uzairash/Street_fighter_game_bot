
Data Generating and Data Loading:
Controller.py contains the details to save the moves in .csv file and everytime the new match was played the data gets appended. The aboe data is used for training after some preprocessing.

Model Training:
On the dataset generated above, random forest model is used to train on dataset. Also the prebuilt model has the predict function that is used to predict on the test data. Traintestsplit a function of scikit-learn library is used to split the dataset into 80% train data and 20% test data. The model is used to predict only the moves of bot i.e. Up, Down, Left and Right.

