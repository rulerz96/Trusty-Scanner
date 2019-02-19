import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
from sklearn.utils import shuffle

def train_model():
    # Load Url Data
    urls_data = pd.read_csv("database/malware_url_samples.data")
    urls_data = shuffle(urls_data)
    # Labels
    labels = urls_data["label"]

    # Features
    features = urls_data["url"]

    # Using Default Tokenizer
    vectorizer = TfidfVectorizer()

    # Store vectors into X variable as Our XFeatures
    features_transform = vectorizer.fit_transform(features)

    X_train, X_test, y_train, y_test = train_test_split(features_transform, labels, test_size=0.2, random_state=42)

    # Model Building
    model = LogisticRegression()	#using logistic regression
    model.fit(X_train, y_train)

    print("Accuracy ",model.score(X_test, y_test))

    ##save model classifier
    save_file_name = 'model_data/model.pkl'
    pickle.dump(model, open(save_file_name, 'wb'))

    ##save vectorizer in file
    pickle.dump(vectorizer, open('model_data/vectorizer.pkl', 'wb'))

def load_model_and_predict(model_name, vectorizer_file, site):
    load_model_file = pickle.load(open(model_name, 'rb'))
    load_vectorizer = pickle.load(open(vectorizer_file, 'rb'))
    test_site = site
    test_site = load_vectorizer.transform(test_site)
    prediction = load_model_file.predict(test_site)
    return prediction

#train_model()
