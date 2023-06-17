# Spotify-ETL-Airflow

# Spotify ETL with Airflow

This project demonstrates an Extract, Transform, Load (ETL) process for retrieving data from the Spotify API, transforming it, and loading it into a Google Cloud Storage bucket. The ETL process is orchestrated using Apache Airflow.

## Project Structure

The project consists of the following files:

- `Spotify_DAG.py`: The Airflow DAG (Directed Acyclic Graph) file that defines the ETL workflow and tasks.
- `Spotify_ETL.py`: Python script containing functions for interacting with the Spotify API, performing data extraction, transformation, and loading.
- `.env`: Environment file containing sensitive information such as Spotify client credentials.
- `keys.json`: JSON file containing the credentials for accessing the Google Cloud Storage bucket.
- Other necessary configuration files.

## Setup Instructions

To set up and run this project, follow these steps:

1. Clone the repository to your local machine.
2. Set up a virtual environment and activate it.
3. Install the required dependencies listed in the `requirements.txt` file.
4. Configure your Spotify API credentials and Google Cloud Storage credentials by filling in the necessary information in the `.env` and `keys.json` files, respectively.
5. Update the Airflow configuration file (`airflow.cfg`) with the appropriate settings.
6. Start the Airflow webserver and scheduler.
7. Trigger the Spotify ETL DAG in Airflow to initiate the ETL process.

Make sure to refer to the project documentation and relevant guides for more detailed instructions on setting up and running the project.

## Contributions

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize this README file according to the specific details of your project. Provide clear instructions for setting up and running the project, mention any dependencies, and include relevant links to documentation or resources.
