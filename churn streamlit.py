# churn_streamlit_app.py

import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

st.title("Expresso Churn Prediction")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Mapping for TENURE
    tenure_mapping = {
        'K > 24 month': 8,
        'J 21-24 month': 7,
        'I 18-21 month': 6,
        'H 15-18 month': 5,
        'G 12-15 month': 4,
        'F 9-12 month': 3,
        'E 6-9 month': 2,
        'D 3-6 month': 1
    }

    # Columns to use
    cols_to_use = ['TENURE', 'REGION', 'CHURN']  # add other important columns if needed

    # Read CSV in chunks
    chunksize = 50000
    df_list = []

    for chunk in pd.read_csv(uploaded_file, usecols=cols_to_use, chunksize=chunksize):
        chunk = chunk.dropna()
        chunk['TENURE'] = chunk['TENURE'].map(tenure_mapping)
        chunk = pd.get_dummies(chunk, columns=['REGION'], drop_first=True)

        # Future-proof boolean conversion
        bool_cols = chunk.select_dtypes(include='bool').columns
        chunk[bool_cols] = chunk[bool_cols].astype(int)

        df_list.append(chunk)

    # Combine all chunks
    df1 = pd.concat(df_list, ignore_index=True)

    # Optional: downcast numeric columns
    for col in df1.select_dtypes(include='float'):
        df1[col] = pd.to_numeric(df1[col], downcast='float')
    for col in df1.select_dtypes(include='int'):
        df1[col] = pd.to_numeric(df1[col], downcast='integer')

    st.success("Data loaded and processed successfully!")

    # Features and target
    X = df1.drop('CHURN', axis=1)
    y = df1['CHURN']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train RandomForest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    conf_matrix = metrics.confusion_matrix(y_test, y_pred)

    st.write(f"**Accuracy:** {accuracy:.2f}")
    st.write("**Confusion Matrix:**")
    st.write(conf_matrix)
