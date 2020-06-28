from db_commands import create_all_tables, create_database, delete_tables, drop_database, populate_queue


drop_database()
create_database()
delete_tables()
create_all_tables()
populate_queue(upper_limit=20000)
