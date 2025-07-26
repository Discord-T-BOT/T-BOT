import sqlite3
class eco:
    def __init__(self) -> None:

        DB_FILE = 'database/eco.db'
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        # テーブルの作成
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eco (
                user_id TEXT PRIMARY KEY,
                amount INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def get_eco(self, user_id:str) -> int:
        self.cursor.execute('SELECT amount FROM eco WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def update_eco(self,user_id:str, amount:int):
        if self.get_eco(user_id) == 0:
            self.cursor.execute('INSERT INTO eco (user_id, amount) VALUES (?, ?)', (user_id, amount))
        else:
            self.cursor.execute('UPDATE eco SET amount = ? WHERE user_id = ?', (amount, user_id))
        self.conn.commit()

    def create_eco(self, user_id:str):
        self.update_eco(user_id=user_id, amount=0)
    
    def delete_eco(self, user_id:str) -> bool:
        self.cursor.execute("SELECT amount FROM eco WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        
        if result is None:
            return False
        else:
            self.cursor.execute('DELETE FROM eco WHERE user_id = ?',(user_id,))
            self.conn.commit()
            return True