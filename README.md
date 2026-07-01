Overview

This project implements an end-to-end data engineering pipeline designed to extract, load, and transform (ELT) cast (character) elements of the popular show ‘Rick & Morty’. It leverages Python for API interaction, Docker for containerised database management, and dbt (data build tool-Postgresql) for data modeling and cleaning.

—------------------------------------------------------------------------------------------------------------------------

The Remit

The objective of this exercise is to bring in important information regarding the characters from the appropriate API (‘The Rick and Morty API’), so we can use this to cross reference the exposure they have been given (% of episodes they have appeared in) and an average of what has costed the production company over the lifespan of it being on the air.

—------------------------------------------------------------------------------------------------------------------------

The Stack

Language: Python 3.14 (used for API requests and data normalisation)

Database: PostgreSQL (deployed via Docker Compose for a consistent local environment), to bring in appropriate columns and also custom columns for the ‘exposure %’ and monetary cost per character - used CTEs to achieve the requirements. 

Data Transformation: dbt (used to transform raw API responses into a clean, production-ready table)

Secret Management: A .env file is used to securely store API keys and database credentials, ensuring they are not exposed in the source code. Also, added ‘logs/’, ‘.vscode/’, ‘target/’, ‘dbt_packages/’, ‘--pycache–’.

How the Pipeline Works Extraction: The Python script located in the scripts/ directory connects to the Rick and Morty API service. It queries the relevant endpoint for the character information.

Normalisation: During the Python execution, raw JSON responses from the API are parsed and normalised into a format suitable for database ingestion.

Transformation: Using dbt, the raw data is cleaned and restructured. The final output is a materialised table containing the required columns and metrics.

—------------------------------------------------------------------------------------------------------------------------

The Structure

models/: Contains the core logic for your transformations. The.sql defines the SQL logic required to clean the data and select the final output columns, as well as custom columns.

pipelines/: Holds py, the core Python script responsible for fetching data and interacting with the database.

dbt_project.yml: Defines the project configuration for dbt/postgres.
sources.yml: Contains name, schema, tables required

.gitignore: Ensures that sensitive files, information are never uploaded to GitHub.

—------------------------------------------------------------------------------------------------------------------------

The Logic

Python - ‘The E and L in ELT’

Imported the following packages to achieve the objective:

-pandas (as pd)
-requests
-json_normalize (from the pandas package)
-os
-load_dotenv (from dot_env)

Began by utilising load_dotenv to bring in .env variables we do not want made public (API information mainly.

A blank list was created, as we have to paginate multiple pages (47) in a loop, to ensure all data is captured.

A while function is used, stating this should respond with the url request for the API and store this as a response; if the grab is successful (200) the response is captured as a variable again, as data. A .extend along with ‘[‘info’][‘next’]’ (API next page requirement), is used to paginate into the list.

The result is then captured as ‘df’ utilising a .json_normalize.

The SQL engine is then created using ‘create_engine’ and the credentials are brought in with a .getenv for confidentiality. 

This is then put into my Docker container for postgres with a ‘to_sql’ call.

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

dbt/postgres - ‘The T in ELT’

Within the dbt folder (models/staging) SQL query is executed to transform the API data.

The CTE ‘WITH’ is used to create a ‘base_data’. This SELECTs the name, status, species, gender for columns; custom column also executed to return episode count - this is achieved by parsing the values between commas and then adding 1 to return the count of episodes per character, this is stored as ‘episode_count.

Further query called ‘final_metrics’ made, whilst aliasing the ‘base_data’ as bd. This is to achieve two further required columns in the ask, ‘exposure_ratio’ and ‘total_voice_actor_pay’. Column ‘exposure_rastio’ uses the TOTAL episode count to date that have aired and this is used as a denominator against the individual characters count - this is then stored as decimal to 2 places. Column ‘total_voice_actor_pay’ takes a static figure of 50000 (average pay per episode per actor) and is then multiplied against the individual episode count, this is stored as an integer.

Final execution is a SELECT * of the final_metrics table.
