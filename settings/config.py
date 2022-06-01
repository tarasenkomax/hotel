from environs import Env

env = Env()
env.read_env()

# Postgres
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

# SMTP
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_USE_TLS = env.str("EMAIL_USE_TLS")
EMAIL_PORT = env.str("EMAIL_PORT")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
