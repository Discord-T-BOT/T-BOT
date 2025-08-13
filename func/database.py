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

class tag:
    def __init__(self) -> None:

        DB_FILE = '../tag.db'
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        # テーブルの作成
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag (
                name TEXT PRIMARY KEY,
                invite TEXT,
                message_id TEXT
            )
        ''')
        self.conn.commit()
    
    def get_tag(self, name:str) -> int:
        self.cursor.execute('SELECT invite,message_id FROM tag WHERE name = ?', (name,))
        return self.cursor.fetchone()
    
    def update_invite(self, name:str, invite:str):
        self.cursor.execute('UPDATE tag SET invite = ? WHERE name = ?', (invite, name))
        self.conn.commit()

    def create_tag(self, name:str, invite:str, message_id:str):
        self.cursor.execute('INSERT INTO tag (name, invite, message_id) VALUES (?, ?, ?)', (name, invite, message_id))
        self.conn.commit()
    
    def delete_tag(self, name:str):
        self.cursor.execute('DELETE FROM tag WHERE name = ?',(name,))
        self.conn.commit()

class set_sc_ex:
    def __init__(self) -> None:
        DB_FILE = 'database/settings.db'
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scex (
                channel_id TEXT PRIMARY KEY,
                data TEXT
            )
        ''')
    
    def add_channel(self, id:str):
        self.cursor.execute('INSERT INTO scex (channel_id, data) VALUES (?,?)', (id,"true"))
        self.conn.commit()
    def del_channel(self, id:str):
        self.cursor.execute('DELETE FROM scex WHERE channel_id = ?',(id,))
        self.conn.commit()
    def get_channel(self, id:str):
        self.cursor.execute('SELECT data FROM scex WHERE channel_id = ?', (id,))
        return self.cursor.fetchone()

class set_auto_pub:
    def __init__(self) -> None:
        DB_FILE = 'database/settings.db'
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pub (
                channel_id TEXT PRIMARY KEY,
                data TEXT
            )
        ''')
    def add_channel(self, id:str):
        self.cursor.execute('INSERT INTO pub (channel_id, data) VALUES (?,?)', (id,"true"))
        self.conn.commit()
    def del_channel(self, id:str):
        self.cursor.execute('DELETE FROM pub WHERE channel_id = ?',(id,))
        self.conn.commit()
    def get_channel(self, id:str):
        self.cursor.execute('SELECT data FROM pub WHERE channel_id = ?', (id,))
        return self.cursor.fetchone()