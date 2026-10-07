import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv(
    'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
    '''
# My question one: Did men in first class have a higher survival rate than women in third class?

'''
)
# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)


st.write("My findings are that the last-name count agree with the data table above.")
st.write(last_names())


st.write(
    '''
# My question two: Were there any members of a family with greater than three members on board where only one survived?
'''
)
# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
    '''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)
