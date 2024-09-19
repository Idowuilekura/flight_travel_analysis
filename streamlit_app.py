import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import OrdinalEncoder

# Function to read and clean CSV file
@st.cache_data
def read_clean_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if pd.api.types.is_integer_dtype(df['DepartureTime']):
        df['DepartureTime'] = pd.to_datetime(df['DepartureTime'], unit='s', errors='coerce')
    else:
        df['DepartureTime'] = pd.to_datetime(df['DepartureTime'], errors='coerce')
    
    if pd.api.types.is_integer_dtype(df['ArrivalTime']):
        df['ArrivalTime'] = pd.to_datetime(df['ArrivalTime'], unit='s', errors='coerce')
    else:
        df['ArrivalTime'] = pd.to_datetime(df['ArrivalTime'], errors='coerce')
    df['DepartureTime'] = pd.to_datetime(df['DepartureTime'])
    df['ArrivalTime'] = pd.to_datetime(df['ArrivalTime'])
    df_numeric = df.select_dtypes(exclude=['object','datetime64[ns, UTC]'])

    for col in df_numeric.columns:
        get_negative_values = df_numeric[col] < 0
        sum_negative_values = sum(get_negative_values)
        total_records_column = len(df_numeric[col])
        if sum_negative_values > 0:
            print(f"column {col} has {sum_negative_values} negative values out of {total_records_column}, which should not be")
    return df

# Light exploration function
def light_exploration(df: pd.DataFrame) -> None:
    st.write(df.head())
    st.write(df.info())
    plt.figure(figsize=(10, 6))
    sns.boxplot(df['HistoricalSpend'])
    plt.title("Boxplot of Historical Spend")
    st.pyplot(plt)

# Visualization Functions
def plot_top_5_by_sum(df: pd.DataFrame, group_col: str, sum_col: str):
    grouped_data = df.groupby(group_col)[sum_col].sum().reset_index()
    top_5 = grouped_data.sort_values(by=sum_col, ascending=False).head(5)
    
    plt.figure(figsize=(10, 6))
    plt.barh(top_5[group_col], top_5[sum_col], color='blue')
    plt.title(f'Top 5 {group_col} by Sum of {sum_col}')
    plt.xlabel(f'Sum of {sum_col}')
    st.pyplot(plt)

def plot_top_5_counts(df: pd.DataFrame, col: str):
    top_5 = df[col].value_counts().head(5)
    plt.figure(figsize=(10, 6))
    top_5.plot(kind='barh', color='green')
    plt.title(f'Top 5 Most Frequent Values in {col}')
    st.pyplot(plt)

# Prediction Functions
def transform_categoric(df: pd.DataFrame):
    col_encoder_dict = dict()
    df_copy = df.copy()
    df_copy_string = df_copy.select_dtypes(include=['object'])
    for col in df_copy_string:
        encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        df_copy[col] = encoder.fit_transform(df_copy[col].to_frame())
        col_encoder_dict[f"{col}_encoder"] = encoder
    return df_copy, col_encoder_dict

def save_encoder(encoder_dict: dict, path: str):
    with open(path, 'wb') as handle:
        pickle.dump(encoder_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_encoder(path: str):
    with open(path, 'rb') as handle:
        return pickle.load(handle)
model_path = os.path.jpin(os.getcwd(), "best_model.pkl")
def load_model(path: str):
    with open(path, 'rb') as handle:
        return pickle.load(handle)

def cat_days_predict(col):
    if col <= 7:
        return "Within 1 week"
    elif col <= 30:
        return "Within 1 month"
    elif col <= 150:
        return "2-5 months"
    elif col <= 365:
        return "6-12 months"

def add_weekday_info(df: pd.DataFrame, datetime_col: str):
    df['Weekday_Number'] = df[datetime_col].dt.weekday
    df['Day_Type'] = df['Weekday_Number'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    return df

# Main Streamlit Application
st.title("Flight Data Analysis and Prediction App")

# Select analysis or prediction mode
option = st.radio("Choose an option:", ("Upload CSV for Analysis", "Make a Prediction"))

if option == "Upload CSV for Analysis":
    csv_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if csv_file:
        df = read_clean_csv(csv_file)

        # Light Exploration
        if st.checkbox("Show Data Exploration"):
            light_exploration(df)

        # Visualizations
        if st.checkbox("Show Top 5 Routes by Sum and Count"):
            plot_top_5_by_sum(df, "Carrier", "HistoricalSpend")
            plot_top_5_counts(df, "Carrier")

        # Future option for training the model
        # st.write("You can train your model here (future implementation)")

else:
    # Prediction section
    model = load_model(model_path)
    encoder_dict = load_encoder("encoder.pkl")

    # User input for prediction
    origin = st.text_input("Origin")
    destination = st.text_input("Destination")
    carrier = st.text_input("Carrier")
    duration = st.number_input("Duration")
    booking_lead_time = st.number_input("Booking Lead Time")
    number_of_stops = st.number_input("Number of Stops")
    leg_count = st.number_input("Leg Count")
    departure_time = st.date_input("Departure Time")
    arrival_time = st.date_input("Arrival Time")

    if st.button("Predict"):
        df_input = pd.DataFrame({
            "Origin": [origin],
            "Destination": [destination],
            "Carrier": [carrier],
            "Duration": [duration],
            "BookingLeadTime": [booking_lead_time],
            "NumberOfStops": [number_of_stops],
            "LegCount": [leg_count],
            "DepartureTime": [departure_time],
            "ArrivalTime": [arrival_time]
        })
        df_input['DepartureTime'] = pd.to_datetime(df_input['DepartureTime'])
        df_input['ArrivalTime'] = pd.to_datetime(df_input['ArrivalTime'])
        df_input, _ = transform_categoric(df_input)
        df_input = add_weekday_info(df_input, "DepartureTime")
        df_input['is_festive_season'] = df_input["DepartureTime"].apply(lambda x: 'festive_season' if x.month == 12 or x.month == 1 else 'not_festive_season')
        df_input['booking_lead_days_category'] = df_input["BookingLeadTime"].apply(lambda x: cat_days_predict(x))

        for col in df_input.select_dtypes(include=["object"]):
            test_col_encoder = encoder_dict.get(f"{col}_encoder")
            if test_col_encoder:
                df_input[col] = test_col_encoder.transform(df_input[col].to_frame())
        df_input = df_input.drop(['DepartureTime', 'ArrivalTime'], axis=1)
        desired_order = [
            "Origin", "Destination", "Carrier", "Duration", "BookingLeadTime", 
            "NumberOfStops", "LegCount", "booking_lead_days_category", 
            "is_festive_season", "Weekday_Number", "Day_Type"
        ]
        df_input = df_input[desired_order]
        prediction = model.predict(df_input)
        st.write(f"Predicted Historical Spend: {prediction[0]}")

