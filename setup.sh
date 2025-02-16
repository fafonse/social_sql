
rm -f social.db

sqlite3 social.db < schema.sql

python3 init.py
