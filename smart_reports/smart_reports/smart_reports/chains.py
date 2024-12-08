import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def generate_home_dashboard_queries(self, metadata):
        prompt_extract = PromptTemplate.from_template(
            """
            ### DATABASE METADATA:
            {db_metadata}
            ### INSTRUCTION:
            generate some sql queries to calculate the important metrics with appropriate aliases to column names
            return a json with the generated queries, visualization chart type that best shows it like "bar chart","single value","pie chart","line chart","heatmap", label_column, value_column and a title to the chart
            Do not show more than 30 datapoints in each chart if it has more
            appropriately order the dataset in asc or desc
            Only return the valid JSON as an array.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"db_metadata": metadata})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to generate queries.")
        return res if isinstance(res, list) else [res]
    
    def generate_explore_response(self, metadata, query):
        prompt_extract = PromptTemplate.from_template(
            """
            ### DATABASE METADATA:
            {db_metadata}
            ### INSTRUCTION:
            using the db data provided, generate one sql query for this: {db_query}
            Ensure the columns are available in the tables
            Show data as table if it has more than 2 columns
            appropriately order the dataset in asc or desc
            return a json with the generated query, visualization chart type chart_type that best shows it like "table", "bar chart","single value","pie chart","line chart","heatmap", label_column, value_column and a title to the chart
            Only return the valid JSON as an array.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"db_metadata": metadata, "db_query": query})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to generate queries.")
        return res if isinstance(res, list) else [res]

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
    