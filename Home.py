import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")

dataframe_options = {
    "Experiment 1": "./plot_data/experiment_1/experiment_1.csv",
    "Experiment 2": "./plot_data/experiment_2/experiment_2.csv",
    "Experiment 3": "./plot_data/experiment_3/experiment_3.csv",
    "Experiment 4": "./plot_data/experiment_4/experiment_4.csv",
    "Experiment 5": "./plot_data/experiment_5/experiment_5.csv",
    "Experiment 6": "./plot_data/experiment_6/experiment_6.csv",
}
dataframe_descriptions = {
    "Experiment 1": "./plot_data/experiment_1/description_experiment_1.md",
    "Experiment 2": "./plot_data/experiment_2/description_experiment_2.md",
    "Experiment 3": "./plot_data/experiment_3/description_experiment_3.md",
    "Experiment 4": "./plot_data/experiment_4/description_experiment_4.md",
    "Experiment 5": "./plot_data/experiment_5/description_experiment_5.md",
    "Experiment 6": "./plot_data/experiment_6/description_experiment_6.md",
}
experiments_name = {
    "Experiment 1": "Experiment 1",
    "Experiment 2": "Experiment 2",
    "Experiment 3": "Experiment 3",
    "Experiment 4": "RegressionRecommender with RandomForestsRegressor",
    "Experiment 5": "RegressionRecommender with XGBoost",
    "Experiment 6": "RegressionRecommender with SVR",
}
selected_dataframe = st.selectbox("Select Experiment", options=list(dataframe_options.keys()))

@st.cache_data
def load_data(path: str):
    quantifiers_to_remove = [
        '(KNN)Top-2',
        '(KNN)Top-4',
        '(KNN)Top-6',
        '(KNN)Top-7',
        '(KNN)Top-8',
        '(KNN)Top-9',
        '(KNN)Top-10',
        '(KNN)Top-11',
        '(KNN)Top-1+W',
        '(KNN)Top-2+W',
        '(KNN)Top-4+W',
        '(KNN)Top-6+W',
        '(KNN)Top-7+W',
        '(KNN)Top-8+W',
        '(KNN)Top-9+W',
        '(KNN)Top-10+W',
        '(KNN)Top-11+W',
        '(REG)Top-2',
        '(REG)Top-4',
        '(REG)Top-6',
        '(REG)Top-7',
        '(REG)Top-8',
        '(REG)Top-9',
        '(REG)Top-10',
        '(REG)Top-11',
        '(REG)Top-1+W',
        '(REG)Top-2+W',
        '(REG)Top-4+W',
        '(REG)Top-6+W',
        '(REG)Top-7+W',
        '(REG)Top-8+W',
        '(REG)Top-9+W',
        '(REG)Top-10+W',
        '(REG)Top-11+W',
    ]
    data = pd.read_csv(path)
    data = data[~data['quantifier'].isin(quantifiers_to_remove)]
    return data

def interactive_boxplot(data):
    st.subheader(f":green[{experiments_name[selected_dataframe]}]")
    checkbox_col, boxplot_col = st.columns([1, 4])
    
    default_options = ['ACC', 'CC', 'DyS', 'HDy', 'MAX', 'MS', 'PACC', 'PCC', 'SMM', 'SORD', 'X']
    default_data = data[data['quantifier'].isin(default_options)]
    to_select_data = data[~data['quantifier'].isin(default_options)]

    with checkbox_col:
        filter_options = to_select_data['quantifier'].unique()
        filter_options = sorted(filter_options, key=lambda x: ('+W' in x, x))
        selected_filters = st.multiselect('Recommender methods', filter_options)
    to_select_data = to_select_data[to_select_data['quantifier'].isin(selected_filters)]
    filtered_data = pd.concat([default_data, to_select_data])

    with boxplot_col:
        filtered_data['error_rank'] = filtered_data.groupby(['dataset'], as_index=False)['abs_error'].rank(method='average', ascending=True)
        order = filtered_data.groupby('quantifier')['error_rank'].mean().sort_values().index

        fig = px.box(filtered_data, x='quantifier', y='error_rank', color='quantifier', category_orders={'quantifier': order},
                     labels={'quantifier': 'Quantifiers', 'error_rank': 'Avg. ranking'})
        # fig.update_layout(width=1200, height=800)  # Adjust width and height of the figure
        # fig.update_yaxes(range=[0, filtered_data['error_rank'].max() * 0.6])  # Adjust y-axis range to scale down the boxes

        st.plotly_chart(fig)

data = load_data(dataframe_options[selected_dataframe])
interactive_boxplot(data)

# st.title("Experiment Explorer") 
if "show_description" not in st.session_state:
    st.session_state.show_description = True

def toggle_description():
    st.session_state.show_description = not st.session_state.show_description

if st.button("Experiment description"):
    toggle_description()

if st.session_state.show_description:
    description_file = dataframe_descriptions[selected_dataframe]
    with open(description_file, "r") as file:
        description = file.read()
    st.markdown(description)