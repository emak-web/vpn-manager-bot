from config_reader import config


def generate_config(privatekey: str, ip: str, username: str, index: int):
    
    with open(config.sample_config_path, 'r') as file:
        sample_config = file.read()

    sample_config = sample_config.replace('<privatekey>', privatekey)
    sample_config = sample_config.replace('<ip>', ip)

    file_name = f'{username}_{index+1}.conf'

    with open(f'{config.conf_dir}/{file_name}', 'w') as file:
        file.write(sample_config)

    return file_name

