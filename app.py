# import things
import streamlit as st
import pandas as pd
import os
from io import BytesIO



# Set up the App
st.set_page_config(page_title= "💿⚙🛠 Data Sweeper" , layout= "wide")
st.markdown("""
<style>
/* Background Color */
.stApp {
    background-color:#f5cac3;
    color:#03045e;
    font-family: 'Poppins', sans-serif;
}
</style>
""", unsafe_allow_html=True)


st.title("💿 Data Sweeper:")
st.write("🔁 Convert between CSV and Excel formats with built-in data cleaning and visualization features.")

uploaded_files = st.file_uploader("📁 Upload your files (CSV , Excel or json):", type=["csv","xlsx", "json" ], accept_multiple_files= True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
          df = pd.read_csv(file) 
        elif file_ext  == ".xlsx":
          df = pd.read_excel(file)
        elif file_ext  == ".json":
          df = pd.read_json(file) 
        else:
          st.error(f"❌ Unsupported file type: {file_ext}")
          continue


        # Display information about the file
        st.write(f"📄File name: {file.name}")
        st.write(f"**File size** {file.size/1024}")

        # show 5 rows of our def
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())


        #Options for data cleaning
        st.subheader("🚯 Data Cleaning Options :")
        if st.checkbox(f"Clean Data for {file.name}"):
           col1 , col2 = st.columns(2)

           with col1:
               if st.button(f"🧹 Remove Duplicate from  {file.name}"):
                  df.drop_duplicates(inplace=True)
                  st.write("✅ Duplicates Removed!")

           with col2:
                if st.button(f"🔍 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values have been Filled!")



        #Choose specificc Columns to keep or convert 
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns , default = df.columns)
        df = df[columns]

         # Create Data Visualization 
        st.subheader("📊 Data Visualization") 
        if st.checkbox(f"Start Visualization for {file.name}") :
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:])


        # Convert the file => CSV OR EXCEL  

        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "EXCEL", "JSON"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "EXCEL":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
               
            
            elif conversion_type == "JSON":
                df.to_json(buffer, index=False)
                file_name = file.name.replace(file_ext, ".json")
                mime_type = "json"
                buffer.seek(0)


                # Download Button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type.lower()}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )


st.success("🎉All files processed!!✨ ")  

 
                    


