import streamlit as st
from google.cloud import bigquery
from PIL import Image
import base64
import os



# Function to create the BigQuery client
def create_bigquery_client():
    creds = {
        "type": "service_account",
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN"),
    }
    client = bigquery.Client.from_service_account_info(creds)
    return client

# Function to query data from BigQuery
def query_data(client, sale_amt_range, num_bedrooms, state):
    # Build SQL query based on input parameters
    query = f"""
        SELECT s.*, pd.Bed, pd.state
        FROM `housingdataanalysis.HousingData.Sale` s
        LEFT JOIN `housingdataanalysis.HousingData.PropertyDetails` pd
        ON s.Property_id = pd.Property_id
        WHERE (s.SaleAmt BETWEEN {sale_amt_range[0]} AND {sale_amt_range[1]})
        AND (pd.Bed = {num_bedrooms} OR {num_bedrooms} IS NULL)
        AND (pd.state = '{state}' OR '{state}' IS NULL)
    """
    # Execute query
    result = client.query(query)
    # Convert result to DataFrame
    data = result.to_dataframe()
    return data

def image_to_base64(image):
    image_base64 = base64.b64encode(image.tobytes()).decode("utf-8")
    return image_base64





import streamlit as st

def home_page():
    # Set page title
    st.title("Welcome to RelocationNavigator")

    # Introduction text
    st.markdown(
        """
        Discover a unified platform that offers detailed insights into housing prices, safety, and demographics 
        across various regions in the United States. **RelocationNavigator** simplifies complex decisions by 
        providing easy comparisons of affordability and living conditions, empowering users with data-driven analysis.

        **Why:**

        - **Simplify Relocation Decisions:** Tailored for job seekers and students, **RelocationNavigator** simplifies 
          the often complex process of deciding where to move.
        - **Empowerment Through Data:** Access detailed information on safety and the cost of living to make informed 
          decisions that align with your preferences and priorities.
        - **Data-Driven Decision Making:** Harness the power of data to make informed choices about your relocation, 
          ensuring a smooth transition to your new home.

        **How:**

        - **Real Estate Insights:** Leveraging the Attom API, **RelocationNavigator** provides real-time data on housing 
          prices, allowing you to explore the real estate landscape across the nation.
        - **Crime Data Analysis:** Utilizing USAFacts data, our platform offers a comprehensive overview of safety, 
          helping you understand the security landscape in different regions.
        - **Interactive Dashboard:** Our user-friendly interface presents all the crucial details in an interactive 
          dashboard, making it easy to explore and compare various aspects of relocation.
        - **Recommendation System:** Beyond data presentation, **RelocationNavigator** acts as a recommendation system, 
          guiding you towards locations that match your preferences and requirements.

        Make your relocation journey smoother, safer, and more informed with **RelocationNavigator**. Your next 
        adventure awaits! 🚀
        """
    )

    # Image
    st.image("images/home.jpg", use_column_width=True, caption="Image Caption")






# Architecture Page
def architecture_page():
    st.title("Architecture Page")
    st.write("Information about the architecture of the Housing Data App goes here.")




def recommendation_page():
    st.title("Recommendation Page")
    st.write("Input parameters for recommendation:")

    # Get or create the BigQuery client in the session state
    if 'client' not in st.session_state:
        st.session_state.client = create_bigquery_client()

    # Input fields
    sale_amt_range = st.slider("Sale Amount Range", 0, 1000000, (0, 1000000))
    num_bedrooms = st.number_input("Number of Bedrooms", min_value=0, step=1)

    # Dropdown list for states
    states = [
        "Rhode Island", "New Hampshire", "Maine", "Virginia", "North Carolina",
        "Alabama", "Tennessee", "Mississippi", "Indiana", "Wisconsin",
        "North Dakota", "Montana", "Wyoming", "Idaho", "New Mexico", "Alaska",
        "Delaware", "West Virginia", "Ohio", "Missouri", "Utah", "California",
        "Hawaii", "Michigan", "Louisiana", "Vermont", "Illinois", "Minnesota",
        "Washington", "Kansas", "Pennsylvania", "Connecticut", "New Jersey",
        "New York", "Maryland", "South Carolina", "Georgia", "Florida", "Iowa",
        "South Dakota", "Nebraska", "Arkansas", "Oklahoma", "Texas", "Colorado",
        "Nevada", "Oregon"
    ]

    state = st.selectbox("Select State", states)

    # Button to trigger recommendation
    if st.button("Get Recommendations"):
        # Get data based on input
        recommendations = query_data(st.session_state.client, sale_amt_range, num_bedrooms, state)

        # Display recommendations
        st.subheader("Recommendations:")
        st.dataframe(recommendations)



# Main function
def main():
    st.sidebar.title("Navigation")
    pages = ["Home", "Architecture", "Recommendation"]
    selection = st.sidebar.radio("Go to", pages)

    if selection == "Home":
        home_page()
    elif selection == "Architecture":
        architecture_page()
    elif selection == "Recommendation":
        recommendation_page()

# Run the app
if __name__ == '__main__':
    main()

