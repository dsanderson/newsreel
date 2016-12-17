from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2:/~/abby', echo=False)

if __name__ == '__main__':
    connection = db_utils.engine.connect()
    connection.close()