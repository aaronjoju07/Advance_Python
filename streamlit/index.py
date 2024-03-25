import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Iris dataset
df = pd.read_csv('/Users/aaronjoju/Documents/Advance_Python/practice/Iris.csv')

# Streamlit app title
st.title("Iris Dataset")

# Sidebar
choice = st.sidebar.selectbox(
    'Which dataset would you like to display?',
    ('All data', 'Sepal', 'Petal'))

# Filter dataframe based on user choice
if choice == 'All data':
    pass
elif choice == 'Sepal':
    df = df[['SepalLengthCm', 'SepalWidthCm', 'Species']]
else:
    df = df[['PetalLengthCm', 'PetalWidthCm', 'Species']]

# Display selected dataset
st.write("### Displaying selected dataset")
st.write(df)

# Plot data if selected
if choice != 'All data':
    st.write("### Visualization")
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Create subplots with 1 row and 2 columns
    if choice == 'Sepal':
        axes[0].scatter(df['SepalLengthCm'], df['SepalWidthCm'],
                        c=pd.factorize(df['Species'])[0], cmap='viridis')
        axes[0].set_xlabel('Sepal Length (cm)')
        axes[0].set_ylabel('Sepal Width (cm)')
        axes[0].set_title('Sepal Dimensions')

        # Add colorbar
        scatter = axes[1].scatter(df['SepalLengthCm'], df['SepalWidthCm'],
                                   c=pd.factorize(df['Species'])[0], cmap='viridis')
        fig.colorbar(scatter, ax=axes[1], label='Species')

        # Hide the second subplot
        axes[1].axis('off')

    else:
        axes[0].scatter(df['PetalLengthCm'], df['PetalWidthCm'],
                        c=pd.factorize(df['Species'])[0], cmap='viridis')
        axes[0].set_xlabel('Petal Length (cm)')
        axes[0].set_ylabel('Petal Width (cm)')
        axes[0].set_title('Petal Dimensions')

        # Add colorbar
        scatter = axes[1].scatter(df['PetalLengthCm'], df['PetalWidthCm'],
                                   c=pd.factorize(df['Species'])[0], cmap='viridis')
        fig.colorbar(scatter, ax=axes[1], label='Species')

        # Hide the second subplot
        axes[1].axis('off')

    st.pyplot(fig)
