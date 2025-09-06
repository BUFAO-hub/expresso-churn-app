import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

st.title("Financial Inclusion Prediction App")

# Upload CSV
uploaded_file = st.file_uploader("Upload Financial Inclusion Dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df = pd.get_dummies(df, columns=['gender_of_respondent'])
    df = pd.get_dummies(df, columns=['marital_status', 'job_type'], drop_first=True)
    df = pd.get_dummies(df, columns=['education_level'], drop_first=True)
    df = df.replace({'Yes': 1, 'No': 0})
    df = df.replace({True: 1, False: 0})
    df['location_type'] = df['location_type'].map({'Rural': 1, 'Urban': 2})
    df['relationship_with_head'] = df['relationship_with_head'].map({
        'Child': 0.5, 
        'Head of Household': 1.0, 
        'Other non-relatives': 0.0, 
        'Other relative': 0.0, 
        'Parent': 1.0, 
        'Spouse': 1.0
    })

    # Features & target
    X = df[['location_type', 'cellphone_access', 'household_size', 'age_of_respondent',
            'relationship_with_head', 'gender_of_respondent_Female',
            'gender_of_respondent_Male', 'education_level_Other/Dont know/RTA',
            'education_level_Primary education', 'education_level_Secondary education',
            'education_level_Tertiary education', 'education_level_Vocational/Specialised training',
            'marital_status_Dont know', 'marital_status_Married/Living together',
            'marital_status_Single/Never Married', 'marital_status_Widowed',
            'job_type_Farming and Fishing', 'job_type_Formally employed Government',
            'job_type_Formally employed Private', 'job_type_Government Dependent',
            'job_type_Informally employed', 'job_type_No Income', 'job_type_Other Income',
            'job_type_Remittance Dependent', 'job_type_Self employed']]

    y = df['bank_account']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)

    st.subheader("Model Accuracy")
    st.write(f"Accuracy: {accuracy:.2f}")

    # Show feature importances
    st.subheader("Feature Importances")
    feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    st.bar_chart(feature_importances)

    # Optional: user input form to test predictions
    st.subheader("Test with Custom Input")
    input_data = {}
    for col in X.columns:
        if df[col].dtype in [int, float]:
            input_data[col] = st.number_input(col, value=float(df[col].median()))
        else:
            input_data[col] = st.selectbox(col, df[col].unique())

    if st.button("Predict"):
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        st.write("Prediction:", "Has Bank Account ✅" if prediction == 1 else "No Bank Account ❌")
