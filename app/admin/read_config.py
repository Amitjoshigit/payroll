
import yaml


# Load configuration from YAML file
with open('config/salary.yaml', 'r') as config_file:
    salary_config = yaml.safe_load(config_file)



with open('format.yaml', 'r') as config_file:
    format_config = yaml.safe_load(config_file)


