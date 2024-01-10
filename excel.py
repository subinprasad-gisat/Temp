import streamlit as st
import openai
import pandas as pd
import time
import re
 
# Set your OpenAI API key
# openai.api_key = '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'
openai.api_key =    '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'
# has context menu
# Deactivate SAP ID:
 
Deactivate_SAP_ID_steps = "1.Access the SAP system.\n2.Navigate to the user management section.\n3.Locate the employee's SAP ID.\n4.Disable or deactivate the SAP ID.\n"
Deactivate_SAP_ID_details = """
-Employee Name
-E-mail Address
-Employee ID
-Manager Name
-Cost Center
-Employee country"""
Firefighter_Access_steps = """1.Access the firefighter access log reporting tool.\n
2.Generate a report for the specified employee.\n
3.Review the log for any suspicious or unauthorized activities.\n"""
Firefighter_Access_details = """
-SAP User ID
-SAP Application
-Role Name
-Start Date"""
InternalSSLTask_steps = """1.Access the internal SSL management system.\n
2.Locate the employee's SSL certificate.\n3.Revoke or disable the SSL certificate.
"""
InternalSSLTask_details = """
-subject name"""
NewcompanycodeSAP_step = """1.Access the SAP system.\n
2.Navigate to the authorization management section.\n
3.Assign the necessary authorizations for the new company code to the employee's SAP ID."""
NewcompanycodeSAP_details = """
-Name of the legal entity
-Company Code Description Name
-Registered address
-City
-Country
-Currency
-Currency of Operation"""
Provide_ESS_Access = """1.Access the ESS (Employee Self-Service) portal.\n
2.Grant the employee access to the required ESS functionalities.\n
3.Set up the necessary permissions and roles."""
Provide_ESS_Access_details = """
-Employee Id"""
Create_SAP_ID = """Access the SAP user management system.\n
Generate a new SAP ID for the employee.\n
Assign the appropriate roles and authorizations to the new SAP ID.\n
"""
Create_SAP_ID_details = """
-Company Code
-IS Retail ECC Instance
-Mobile Number
-Reference User
-Role Name
-Sale Office
-SAP Application
-SAP Details
-User Name"""
 
Task_List= ['Deactivate SAP ID', 'Internal SSL - Task', 'Firefighter Access Log Reporting Task', 'New company code - SAP AUTH', 'Provide ESS Access', 'Create SAP ID']
def read_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
 
    # Extract descriptions from the 'Description' column
    descriptions = df['Description'].tolist()
    task_to_do = df['Task Name'].tolist()
    return descriptions, task_to_do
 
 
def generate_steps(description, task_to_do):
    Action_list=["Deactivate SAP ID","Internal SSL - Task","Firefighter Access Log Reporting Task","New company code - SAP AUTH","Provide ESS Access","Create SAP ID"]
    conversation = [
        {"role": "user",
         "content": f""""Given the following description, identify the relevant task from the list: {description}
 
          Task list:{Task_List}      "    
         """}
    ]
    response1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.0
    )
    task_to_do=response1['choices'][0]['message']['content']
   
    if  "Deactivate SAP ID" in task_to_do:
        generate_steps = "Deactivate SAP ID"
        details = Deactivate_SAP_ID_details
    if "Internal SSL - Task" in task_to_do:
        generate_steps ="Internal SSL - Task"
        details = InternalSSLTask_details
    if "Firefighter Access Log Reporting Task" in task_to_do:
        generate_steps = "Firefighter Access Log Reporting Task"
        details = Firefighter_Access_details
    if "New company code - SAP AUTH" in task_to_do:
        generate_steps = "New company code - SAP AUTH"
        details = NewcompanycodeSAP_details
    if "Provide ESS Access" in task_to_do:
        generate_steps = "Provide ESS Access"
        details = Provide_ESS_Access_details
    if  "Create SAP ID" in task_to_do:
        generate_steps ="Create SAP ID"
        details = Create_SAP_ID_details
    conversation = [
        {"role": "user",
         "content": f"""Extract the following details from the provided description:
         {details}
         Description: {description}
         """}
    ]
    time.sleep(20)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.0
    )
 
    generated_details = response['choices'][0]['message']['content']
    print(generated_details)
    values = generated_details.split("\n")
    return generate_steps, generated_details
 
 
 
 
# ... (Your existing code)
 
def main():
    # Add Streamlit title and file uploader
    st.title("Ticketing System")
 
    # Create a sidebar layout for the Excel file uploader
    with st.sidebar:
        excel_file_path = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
 
    if excel_file_path is not None:
        # Read descriptions from Excel
        dt_excel = pd.read_excel(excel_file_path)
        dt = dt_excel.iloc[:, :4]
        descriptions, task_to_do = read_excel(excel_file_path)
 
        # Generate task names using OpenAI API with a delay
        Steps = []
        detailslist = []
 
        # Add a progress bar
        progress_bar = st.progress(0)
 
        for i, (description, task) in enumerate(zip(descriptions, task_to_do)):
            step, detail = generate_steps(description, task)
            Steps.append(step)
            detailslist.append(detail)
            # Introduce a delay between API calls
           
 
            # Update progress bar
            progress = (i + 1) / len(descriptions)
            progress_bar.progress(progress)
            time.sleep(20)
 
        # Combine descriptions and task names into a DataFrame
        df = pd.DataFrame(
            {'Description': descriptions, 'Action to be taken': Steps, 'Action to be taken on': detailslist})
        result_df = pd.concat([dt, df], axis=1)
 
        # Create a styled DataFrame with background colors
        # styled_df = result_df.style.applymap(lambda x: 'background-color: #ADD8E6', subset=['Action to be taken','Action to be taken on'])
        # styled_df.to_excel("out.xlsx")
       
        # Display the styled DataFrame in Streamlit
        st.write( result_df.to_html(index=False),unsafe_allow_html=True)

 
if __name__ == "__main__":
    main()
 