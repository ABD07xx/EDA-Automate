#Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit.components.v1 as stc 
import io
import matplotlib.pyplot as plt



#Using basic HTML to write the Heading
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Exploratory Data Analysis</h1>
		<h4 style="color:white;text-align:center;">Using Streamlit </h4>
		</div>
		"""
stc.html(html_temp)



#Uploading a CSV or xlsx file
st.markdown("### Upload a CSV or XLSX file.")
uploaded_data = st.file_uploader("", type=['csv','xlsx'])
##Changing the format of uploaded dataframe to pandas dataframe for better Understanding
if uploaded_data is not None:
    df = pd.read_csv(uploaded_data)

#Using a Pre Loaded CSV {mainly for testing purpose}
if uploaded_data is None:
    if st.checkbox("Use Titanic Dataset as Sample Data"):
        df = pd.read_csv('titanic_data.csv')
    else:
        df = None


#Sidebar for Features
st.sidebar.header("Features Available: ")
filter = st.sidebar.multiselect('Select a feature :', ['View the Dataset','Missing Values','Description of Dataset', 
                                                 'Distribution of Features', 'Visulaisations'])

#Defining the functionalities of the filter:
##1. View the Dataset
if df is not None:
    #st.text(filter)
    if ('View the Dataset' in filter):
        rows,columns = df.shape
        st.markdown(f"## Dataset contains {rows} rows and {columns} columns")
        st.dataframe(df)
    
    if('Missing Values' in filter):
        st.markdown("""
                        <div style='background-color: #cc00ff; padding: 10px'>
                            <h2 style='text-align: center'>Handling Missing Values</h2>
                        </div>
                        """, unsafe_allow_html=True)
        if(df.isnull().sum().sum() == 0):
            st.text("No Value is Missingin any row/column.")
        else:
            st.markdown("### Missing Values Table")
            df_temp = pd.DataFrame(df.isnull().sum()).reset_index()
            df_temp['Percentage'] = round(df_temp[0] / df.shape[0] * 100, 2)
            df_temp['Percentage'] = df_temp['Percentage'].astype(str) + '%'
            df_temp = df_temp.rename(columns = {'index':'Feature', 0:'Count of Null values'})
            st.table(df_temp)
            if st.checkbox("Do you want to Drop the Missing Data: "):
                df = df.dropna(axis=0)
                st.header("Missing Values Updated Table")
                st.table(df.isnull().sum())
                st.success("Null Values successfully Dropped.")
                st.info("Please Note that the dataframe with dropped values will only be used when the checkbox is checked. So you can't close the Missing Values fucntion from the Sidebar if you want to use the dataframe with dropped values")
                
            else:
                df= df_temp

    if("Description of Dataset" in filter):
        st.markdown("""
                        <div style='background-color: #cc00ff; padding: 10px'>
                            <h2 style='text-align: center'>Some Basic Information about the Data</h2>
                        </div>
                        """, unsafe_allow_html=True)
        st.text("Descriptive Stats: ")
        st.dataframe(df.describe())
        st.text("Basic information ")
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        
    if("Distribution of Features" in filter):
        #st.write(df.columns.dtype)
        st.markdown("""
                        <div style='background-color: #cc00ff; padding: 10px'>
                            <h2 style='text-align: center'>Distribution of Features</h2>
                        </div>
                        """, unsafe_allow_html=True)
        st.subheader("Select a column:")    
        select = df.select_dtypes(exclude = 'object').columns
        column = st.selectbox("", select, index = len(select) - 1)
        if column:
            sns.set_style('darkgrid')
            sns.set_context('notebook')
            st.subheader(f"Distribution of {column}")
            fig1 = plt.figure()
            sns.kdeplot(df[column])
            st.pyplot(fig1) 

            
#Visualisation will be divided in 3 categories 
#Num2Num
#Num2Cat
#Cat2Cat
    if('Visulaisations' in filter):
        st.text(filter == 'Visulaisations')
        st.markdown("""
                        <div style='background-color: #cc00ff; padding: 10px'>
                            <h2 style='text-align: center'>Visualisations</h2>
                        </div>
                        """, unsafe_allow_html=True)     

        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            x = st.selectbox("Data Type of x Variable ",['Select','Numerical'])
        with col2:
            y = st.selectbox("Data Type of y Variable ",['Select','Numerical','Categorical'])

        if 'Numerical' in x and 'Numerical' in y:
            choice = st.selectbox("Select a Plot: ",['Select','ScatterPlot','Lineplot'])
        
            if 'ScatterPlot' in choice:
                col1, col2, col3 = st.columns([0.4, 0.4, 0.2])

                # col1 x var
                columns_numeric = df.select_dtypes(exclude='object').columns
                col1 = col1.selectbox("X variable", columns_numeric, index=len(columns_numeric) - 1)

                # col2 y var
                columns_numeric_excluded = columns_numeric.drop(col1)
                col2 = col2.selectbox("Y variable", columns_numeric_excluded, index=len(columns_numeric_excluded) - 1)

                # col3 hue
                hue_column = columns_numeric.drop(col1).drop(col2)
                hue_options = ['None'] + hue_column.tolist()
                col3 = col3.selectbox("Hue is", hue_options, index=0)
                
                if col3 == 'None':
                    fig2 = sns.relplot(data=df, x=col1, y=col2)
                else:
                    fig2 = sns.relplot(data=df, x=col1, y=col2, hue=col3)
                st.pyplot(fig2)
            elif 'Lineplot' in choice:
                
                col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
                # col1 x var
                columns_numeric = df.select_dtypes(exclude='object').columns
                col1 = col1.selectbox("X variable", columns_numeric, index=len(columns_numeric) - 1)

                # col2 y var
                columns_numeric_excluded = columns_numeric.drop(col1)
                col2 = col2.selectbox("Y variable", columns_numeric_excluded, index=len(columns_numeric_excluded) - 1)

                # col3 hue
                hue_column = columns_numeric.drop(col1).drop(col2)
                hue_options = ['None'] + hue_column.tolist()
                col3 = col3.selectbox("Hue is", hue_options, index=0)
                if col3 == 'None':
                    sns.set_style('whitegrid')
                    sns.set_context('notebook')
                    fig2 = sns.relplot(data=df, x=col1, y=col2,kind='line')
                else:
                    sns.set_style('whitegrid')
                    sns.set_context('notebook')
                    fig2 = sns.relplot(data=df, x=col1, y=col2, hue=col3,kind='line')
                st.pyplot(fig2)

        elif(('Numerical' in x and 'Categorical' in y) or ('Categorical' in y and 'Numerical' in x)):
            st.info("Please use X variable for catrgorical datatypes and Y variable for numerical datatypes")
            choice = st.selectbox("Select a plot",['Boxplot','Barplot','Pointplot'])
            if 'Boxplot' in choice:
                col1, col2, col3 = st.columns([0.4, 0.4,0.2])

                # col1 x var
                columns_numeric = df.select_dtypes(exclude='object').columns
                col1 = col1.selectbox("X variable", columns_numeric, index=len(columns_numeric) - 1)

                # col2 y var
                columns_numeric_included = df.select_dtypes(include='object').columns
                col2 = col2.selectbox("Y variable", columns_numeric_included, index=len(columns_numeric_included) - 1)

                sns.set_style('whitegrid')
                sns.set_context('notebook')
                fig3 = sns.boxplot(data=df,x=col1,y=col2,saturation=1)
                st.pyplot(fig3.get_figure())

            if 'Barplot' in choice:
                col1, col2, col3 = st.columns([0.4, 0.4, 0.2])

                # col2 x var
                columns_numeric = df.select_dtypes(exclude='object').columns
                col2 = col2.selectbox("Numerical variable", columns_numeric, index=len(columns_numeric) - 1)

                # col1 y var
                columns_numeric_included = df.select_dtypes(include='object').columns
                col1 = col1.selectbox("Categorical variable", columns_numeric_included, index=len(columns_numeric_included) - 1)


                # col3 hue
                hue_column = df.columns.drop(col1).drop(col2)
                hue_options = ['None'] + hue_column.tolist()
                col3 = col3.selectbox("Hue is", hue_options, index=0)

            
                if col3 == 'None':
                    sns.set_style('whitegrid')
                    sns.set_context('notebook')
                    fig3 = sns.barplot(data=df,y=col2, x=col1, saturation=1,palette='Set2')
                    
                else:
                    sns.set_style('whitegrid')
                    sns.set_context('notebook')
                    fig3 = sns.barplot(data=df, y=col2, x=col1, hue=col3,saturation=1,palette='Set2')
            
            
                st.pyplot(fig3.figure)

            if 'Pointplot' in choice:

                col1, col2, col3 = st.columns([0.4, 0.4, 0.2])

                # col2 x var
                columns_numeric = df.select_dtypes(exclude='object').columns
                col2 = col2.selectbox("Numerical variable", columns_numeric, index=len(columns_numeric) - 1)

                # col1 y var
                columns_numeric_included = df.select_dtypes(include='object').columns
                col1 = col1.selectbox("Categorical variable", columns_numeric_included, index=len(columns_numeric_included) - 1)
                st.text(col1+col2)


                # col3 hue
                hue_column = df.columns.drop(col1).drop(col2)
                hue_options = ['None'] + hue_column.tolist()
                col3 = col3.selectbox("Hue is", hue_options, index=0)

            
                if col3 == 'None':
                    sns.set_style('whitegrid')
                    sns.set_context('notebook')
                    fig3 = sns.pointplot(data=df,y=col2, x=col1)
                    
                else:
                    sns.set_style('whitegrid')
                    sns.set_context('notebook')
                    fig3 = sns.pointplot(data=df, y=col2, x=col1, hue=col3)
            
            
                st.pyplot(fig3.figure)

            


            











