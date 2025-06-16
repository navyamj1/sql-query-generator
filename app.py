import os
import streamlit as st 
import google.generativeai as genai
st.set_page_config(page_title="SQL QUERY GENERATOR",page_icon=":robot:")
google_api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=google_api_key)
model=genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

def main():
    st.markdown(
    """
     <div style ="text-align: center;">
        <h1>SQL QUERY GENERATOR</h1>
        <h3> A tool to generate SQL queries for you</h3>
        <h4>with explanations!!</h4>
    </div>
    """,
    unsafe_allow_html=True,
    )
   
    text_input=st.text_area("Enter the query in English")
    submit=st.button("generate SQL query")
    if submit:
       st.spinner("generating SQL query...")
       template="""
            Create a SQL query snippet using the text below without explanations:
            ```
            {input_text}
            ```
        """
       formatted_template=template.format(input_text=text_input)
       response=model.generate_content(formatted_template)
       sql_query=response.text
       sql_query=sql_query.strip().lstrip("```sql").rstrip("```")
       expectedoutput="""
            provide sample table of expected response of this SQL query snippet with no explanation:
            ```
            {sql_query}
            ```
        """
       formatted_expectedoutput=expectedoutput.format(sql_query=sql_query)
       expoutput=model.generate_content(formatted_expectedoutput)
       expoutput=expoutput.text
       
       explanation="""
            provide explanation for the SQL query:
            ```
            {sql_query}
            ```
        """
       formatted_explanation=explanation.format(sql_query=sql_query)
       output=model.generate_content(formatted_explanation)
       output=output.text
       with st.container():
           st.success("SQL query generated. Here's your query:")
           st.code(sql_query,language="sql")
           st.success("Expected output of this query will be:")
           st.markdown(expoutput)
           st.success("Explanation of the query will be:")
           st.markdown(output)
main()