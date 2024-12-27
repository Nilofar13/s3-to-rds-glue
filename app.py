import boto3
import pandas as pd
import sqlalchemy
from botocore.exceptions import NoCredentialsError

# AWS S3 Configuration
s3_client = boto3.client('s3')
bucket_name = 'your-s3-bucket-name'
s3_file_key = 'path/to/your/file.csv'

# AWS RDS Configuration
rds_host = 'your-rds-host'
rds_port = 3306
rds_user = 'your-rds-username'
rds_password = 'your-rds-password'
rds_db = 'your-rds-database'

# AWS Glue Configuration
glue_database = 'your-glue-database'
glue_table_name = 'your-glue-table'

def read_data_from_s3():
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_key)
        df = pd.read_csv(response['Body'])
        return df
    except NoCredentialsError:
        print("Credentials not available")
        return None

def push_data_to_rds(df):
    try:
        engine = sqlalchemy.create_engine(f'mysql+pymysql://{rds_user}:{rds_password}@{rds_host}:{rds_port}/{rds_db}')
        df.to_sql(name='your_table_name', con=engine, if_exists='replace', index=False)
        return True
    except Exception as e:
        print(f"Failed to push data to RDS: {e}")
        return False

def push_data_to_glue(df):
    glue_client = boto3.client('glue')
    try:
        glue_client.create_table(
            DatabaseName=glue_database,
            TableInput={
                'Name': glue_table_name,
                'StorageDescriptor': {
                    'Columns': [{'Name': col, 'Type': 'string'} for col in df.columns],
                    'Location': f's3://{bucket_name}/{s3_file_key}'
                }
            }
        )
        return True
    except Exception as e:
        print(f"Failed to push data to Glue: {e}")
        return False

def main():
    df = read_data_from_s3()
    if df is not None:
        if not push_data_to_rds(df):
            push_data_to_glue(df)

if __name__ == '__main__':
    main()
