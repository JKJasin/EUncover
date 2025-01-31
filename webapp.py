#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from pyvis.network import Network
import json
import ast  
from PIL import Image
from pathlib import Path


#######################
# Page configuration
st.set_page_config(
    page_title="EUncover",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)



#######################
# Load data

base_dir = Path(__file__).parent

logo_path = base_dir / "data" / "logo.svg"
network_path = base_dir / "data" / "ireland_network_data.json"
bio_path = base_dir / "data" / "irelandMEPbio.csv"
declaration_path = base_dir / "data" / "irelandDeclarations.json"
articles_path = base_dir / "data" / "irelandMEPnews.csv"
pipeline_path = base_dir / "data" / "pipeline_detailed.png"


# names for the selection menu
names_list = [
    "Start",
    "Barry Andrews",
    "Lynn Boylan",
    "Nina Carberry",
    "Barry Cowen",
    "Regina Doherty",
    "Luke Ming Flanagan",
    "Kathleen Funchion",
    "Billy Kelleher",
    "Seán Kelly",
    "Michael McNamara",
    "Ciaran Mullooly",
    "Cynthia Ní Mhurchú",
    "Aodhán Ó Ríordáin",
    "Maria Walsh",
]


#######################
# Sidebar
with st.sidebar:
    
    # Load and display our logo
    st.image(logo_path, use_container_width=True, caption="EUncover")
    
    
    st.title('Select an Irish MEP')
    
    # Dropdown for selecting a person
    selected_name = st.selectbox("Select a person:", names_list)

    st.write("The website will display information about the MEP you selected")

    


#######################
######## Plots ########

# Information about the MEP 

# Function to create and render the network
def create_network(network_path, selected_name):
    """
    Generate a network graph for a specific MEP based on selected_name.
    :param network_path: Path to the JSON file containing network data
    :param selected_name: Name of the MEP to generate the network for
    :return: Path to the generated HTML file
    """
    # Load the dataset
    with open(network_path, 'r') as file:
        data = json.load(file)
    
    # Ensure the selected MEP exists in data
    if selected_name not in data:
        st.error(f"No data available for {selected_name}.")
        return None
    
    # Extracting nodes and edges for the selected MEP
    mep_data = data[selected_name]
    
    # Creating a Pyvis Network
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    
    # Adding nodes to the network
    for node in mep_data['nodes']:
        color = "skyblue" if node["type"] == "Person" else "orange" if node["type"] == "Political Party" else \
                "green" if node["type"] == "Political Group" else "purple" if node["type"] == "Think Tank" else \
                "pink" if node["type"] == "Non-Governmental Organization" else "brown" if node["type"] == "Public Service Broadcaster" else \
                "yellow" if node["type"] == "Organization" else "teal" if node["type"] == "Lobbyist" else "grey"
        size = 50 if node['id'] == selected_name else 30  # Larger size for selected MEP
        net.add_node(node['id'], label=node['id'], color=color, size=size)
    
    # Adding edges to the network
    for edge in mep_data['edges']:
        relation = edge.get("relation", "")
        net.add_edge(edge['source'], edge['target'], title=relation)
    
    # Apply styling: Hierarchical layout with straight edges
    net.set_options("""
{
  "physics": {
    "enabled": true,
    "solver": "barnesHut",
    "barnesHut": {
      "gravitationalConstant": -30000,
      "centralGravity": 0.5,
      "springLength": 100,
      "springConstant": 0.02,
      "damping": 0.05
    }
  },
  "layout": {
    "hierarchical": {
      "enabled": false,
      "direction": "DU",
      "sortMethod": "hubsize"
    }
  }
}
""")
    
    # Save the network to an HTML file - needed to display later
    output_file = f"{selected_name.lower().replace(' ', '_')}_network.html"
    net.save_graph(output_file)
    
    return output_file




#######################
#######################
#######################
# Dashboard Main Panel
col = st.columns((1.5, 5, 1.5), gap='medium')

if selected_name == "Start":
    
    # Title
    st.markdown("# **Welcome to EUncover**")
    st.markdown("### *A Student Project from MA Cultural Data & AI at the University of Amsterdam*\n")

    # Project Introduction
    st.markdown("""
    EUncover is a student-led initiative developed as part of the Data Project course for the MA Cultural Data & AI.
    """)

    # Why?
    st.markdown("## **Why?**")
    st.markdown("""
    A 2024 investigation by FollowTheMoney revealed that 25% of Members of the European Parliament (MEPs) were implicated in scandals, often tied to informal networks that influence decision-making. Citizens seeking MEP information are often confronted with the lack of consolidation of helpful but scattered sources, and the lack of visual, network mapping of relations among MEPs. This project aims to address these challenges to promote transparency and accountability for EU citizens.
    """)

    st.markdown("---")

    # How to Use EUncover
    st.markdown("## **How to Use EUncover**")
    st.markdown("""
    ### 1. Select a Name
    - Choose a **Member of the European Parliament (MEP)** from the dropdown list in the Search bar.
    - For the scope of this project due to limited time, **only Irish EU MEPs** will be displayed.

    ### 2. Explore the Network and Background Information
    - **Interact with the visual network** displaying relationships between the chosen MEP and **their family members, lobbyists, political organizations, think tanks, and other affiliated entities**.
    - **Zoom in and out** to navigate the graph.
    - **Hover over nodes** to view details about each entity.
    - **Click on edges** to view the nature of the relationship *(e.g., lobbying meetings, financial connections, institutional roles).*
    - Explore different connections and consider potential influences in **EU policymaking**.

    ### 3. Discover Additional Information
    - At the **top of the page and in the sidebars**, you will find:
    - **Official declarations** made by the MEP.
    - **Recent news articles** related to the MEP.
    - **Other relevant links**.
    - **Analyze** whether there are similarities between **the Network and Official Declarations by the MEP**.
    """)

    st.markdown("---")

    # Data Collection Section
    st.markdown("## **How We Collected Our Data**")
    st.markdown("""
    The data presented on this website was obtained from:
    - **[Integrity Watch EU](https://www.integritywatch.eu/)**
    - **European Parliament Transparency Registers**
    - **Public Open Data Portals**
    - **Wikipedia and Media Wiki API**  
      
    We processed and structured this information to create an interactive visual representation.
    """)
    st.image(pipeline_path, width=900, caption="Overview Data Provenance and Pipeline")

    st.markdown("---")

    # Team Section
    st.markdown("## **Our Team and Contributions**")
    st.markdown("""
    - **Julia Jasińska** - Website development and design, Data management and analysis lead, Data integration, structuring and cleaning (all), Final notebook
    - **Mike Chow** - Graphic design (Data Pipelines), Literature Review (Methodology), Data cleaning and structuring (EU Integrity Watch, Final notebook)
    - **Julia Vos** - Project chairperson, Data collection and cleaning (Wikipedia)
    - **Renzo Pos** - AI utilization and prototyping, Data cleaning and structuring (EP Website, EU Integrity Watch, Wikipedia)
    - **Royanne Ng** - API scraping (Wikipedia), Data collection and cleaning (Wikipedia), Copyediting
    - **Lykke Winther-Bay** - API scraping, Data collection and structuring (News), Core Literature Review 
    """)

    st.markdown("---")

    # Disclaimer Section
    st.markdown("## **Disclaimer**")
    st.markdown("""
    EUncover is a **student research project**, and while we strive for accuracy, the data may have **limitations, biases, or missing information**.
    The visualizations are based on publicly available data, and we encourage further investigation into the relationships presented.
    """)

    st.markdown("---")

    # Contact & Feedback Section
    st.markdown("## **Contact & Feedback**")
    st.markdown("""
    As an academic project, we welcome **feedback, suggestions, and discussions**.
    If you have any questions or would like to know more about the project, feel free to **email me at julia.jasinska@student.uva.nl**.

    🔎 **Start exploring EU politics and influence now!**
    """)
        

else:

    with col[0]:
        st.write(f"#### Information about {selected_name}") 
        

        # Load the CSV data
        df = pd.read_csv(bio_path)

        # Filter the data for the selected person
        filtered_data = df[df['full_name_title'] == selected_name]

            # do we have the data? The selected person needs to exist in "full_name_title"
        if not filtered_data.empty:
            # Extract relevant information
            country = filtered_data['country'].iloc[0]
            national_party = filtered_data['party'].iloc[0]  # Replace with correct column name
            eu_group = filtered_data['eugroup_full'].iloc[0]  # Replace with correct column name
            wikipedia_url = filtered_data['wikipedia_url'].iloc[0]

            # Process committees - parsing the string as Python list (so it does not look ugly)
            raw_committees = filtered_data['committee_full'].iloc[0]
            committees = ast.literal_eval(raw_committees) if raw_committees else []  # Parse the string as a Python list
            committees_display = ", ".join(committees)  # Join the entries with a comma - looks more natural this way

            # Process delegations - same situation as above
            raw_delegations = filtered_data['delegation_full'].iloc[0]
            delegations = ast.literal_eval(raw_delegations) if raw_delegations else []  # Parse the string as a Python list
            delegations_display = ", ".join(delegations)  # Join the entries with a comma

            # Display the information in the desired format
            st.write(f"**Representing Country:** {country}")
            st.write(f"**National party:** {national_party}")
            st.write(f"**EU party:** {eu_group}")
            st.write(f"**EU Committees:** {committees_display}")
            st.write(f"**EU Delegations:** {delegations_display}")
        else:
            st.write(f"No data available for {selected_name}.")

        st.divider()
        
        # Section with links to profiles of selected meps 
        st.write("#### Links to profiles:")

        st.markdown(f"""
        - [Official profiles of EU MEPs](https://www.europarl.europa.eu/meps/en/full-list)
        - [MEP's Wikipedia]({wikipedia_url})
        - [Integrity Watch EU | MEP income](https://www.integritywatch.eu/mepincomes.php)
        """)

        st.divider()

    
        # Load and display the logo
        st.image(logo_path, use_container_width=True, caption="EUncover")
        

    ################## Main Column ########################
    with col[1]:
        st.markdown('#### Declared Interest') # This will show data that the MEP declared officially 

            
        def load_data(declaration_path):
            with open(declaration_path, "r") as f:
                return json.load(f)

        # Function to generate the display - as flexible as possible given the various ways MEPS filled in their forms
        def display_data(selected_name, data):
            st.write(f"#### EU MEP {selected_name} declared:")

            # Extract and display each section of the declaration in a table
            declaration = data["declaration"]

            # Create a table for each category in the JSON file - if infomraiton was not provided the table will not be rendered
            # Occupation/Membership
            
            if declaration["occupation_membership"]:
                st.table(declaration["occupation_membership"])
            else:
                st.write("No occupation membership declared.") # Idea for improvement - would be better to also include title of category in table, but for now it is enough

            # Remunerated Activity
        
            if declaration["remunerated_activity"]:
                st.table(declaration["remunerated_activity"])
            else:
                st.write("No remunerated activities declared.")

            # Membership
        
            if declaration["membership"]:
                st.table(declaration["membership"])
            else:
                st.write("No memberships declared.")

            # Holdings
        
            if declaration["holdings"]:
                st.table(declaration["holdings"])
            else:
                st.write("No holdings declared.")

            # Additional Support
            
            additional_support = declaration["additional_support"]
            if additional_support:
                st.write(additional_support)
            else:
                st.write("No additional support declared.")

            # Private Interests
            
            private_interests = declaration["private_interests"]
            if private_interests:
                st.write(private_interests)
            else:
                st.write("No private interests declared.")

            # Additional Information
        
            additional_info = declaration["additional_information"]
            if additional_info:
                st.write(additional_info)
            else:
                st.write("No additional information provided.")

        # Streamlit app logic - for dynamic dispaly of the above function
        def main():
            
            # Load and display the data
            try:
                merged_data = load_data(declaration_path)
                if selected_name in merged_data:
                    selected_mep_data = merged_data[selected_name]
                    display_data(selected_name, selected_mep_data)
                else:
                    st.error(f"No data found for {selected_name}.")
            except FileNotFoundError:
                st.error(f"Could not find the file at {declaration_path}. Please check the path and try again.")
            except json.JSONDecodeError:
                st.error("The file is not a valid JSON file. Please check the file content.")

    
        if __name__ == "__main__":
            main()

        ################################################
        # Generate and display the network
        st.divider()

        st.markdown('#### MEP Consolidated Interest Map')
        st.write("          🔎  To see labels and relations interact with the graph!")
        st.write("For categories of nodes see the legend below")
        
        if network_path:
            html_file = create_network(network_path, selected_name)
            if html_file:
            
                st.components.v1.html(open(html_file, "r").read(), height=750)
            else:
                st.error("Failed to generate the network visualization.")
        else:
            st.error("No file path provided.")
    
        st.divider()
    
        # Legend of Node types categories
        st.markdown("""
        <div style="padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
            <strong>Legend: Node Types</strong>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><span style="background-color: skyblue; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Person</li>
                <li><span style="background-color: orange; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Political Party</li>
                <li><span style="background-color: green; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Political Group</li>
                <li><span style="background-color: purple; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Think Tank</li>
                <li><span style="background-color: pink; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Non-Governmental Organization</li>
                <li><span style="background-color: brown; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Public Service Broadcaster</li>
                <li><span style="background-color: yellow; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Organization</li>
                <li><span style="background-color: teal; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Lobbyist</li>
                <li><span style="background-color: grey; padding: 5px 10px; border-radius: 3px; margin-right: 10px;"> </span> Other</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    ################### Column Right ######################
    with col[2]:
    
        st.markdown('#### Featured in Articles')

    

        # Load the CSV data
        df = pd.read_csv(articles_path)

        # Filter the data so full name title mathes the selected_name
        filtered_df = df[df['full_name_title'] == selected_name]

        # CSS styling for smaller text with blue font color (to make it pretty)
        st.markdown("""
            <style>
            .small-text {
                font-size: 12px;  /* Smaller font size */
                color: blue;  /* Blue font color */
            }
            .small-text a {
                color: blue;  /* Ensure the links are also blue */
                text-decoration: none;  /* Remove underline from links */
            }
            .small-text a:hover {
                text-decoration: underline;  /* Add underline on hover */
            }
            </style>
        """, unsafe_allow_html=True)

        # Display the titles with clickable links
        st.write(f"**Links to recent news articles:**")

        if filtered_df.empty:
            st.write("This person did not appear in recent news articles.")
        else:
            for index, row in filtered_df.iterrows():
                title = row['title']
                link = row['link']
                st.markdown(
                    f"<p class='small-text'>• <a href='{link}' target='_blank'>{title}</a></p>",
                    unsafe_allow_html=True,
                )
        st.divider()

        st.markdown('#### About this site: ')
        st.write("We believe that transparency empowers citizens to engage more effectively in decision-making. In line with the European Parliament's commitment to transparency, EUncover aims to build greater legitimacy and accountability of Parliament Members to the people they serve.")