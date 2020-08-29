from .connection import connect

def exists(trainer):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
            SELECT * FROM trainer
            WHERE name  = '{trainer}'
        '''
        cursor.execute(query)
        if not cursor.fetchone():
            return False
        return True