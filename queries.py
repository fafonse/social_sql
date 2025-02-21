import sqlite3

class SocialNetwork:
    def __init__(self, db_name="social.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_user(self, email):
        try:
            self.cursor.execute("INSERT INTO Users (email) VALUES (?)", (email,))
            self.conn.commit()
            print(f"User created with email: {email}")
        except sqlite3.IntegrityError:
            print(f"Error: Email {email} is already in use.")

    def create_account(self, email, username):
        self.cursor.execute("SELECT id FROM Users WHERE email = ?", (email,))
        user = self.cursor.fetchone()
        
        if not user:
            print(f"Error: No user found with email {email}.")
            return

        try:
            self.cursor.execute("INSERT INTO Accounts (user_id, username) VALUES (?, ?)", (user[0], username))
            self.conn.commit()
            print(f"Account '{username}' created for {email}.")
        except sqlite3.IntegrityError:
            print(f"Error: Username {username} is already taken.")
            
    def create_post(self, account_id, text):
        self.cursor.execute("INSERT INTO Posts (account_id, content) VALUES (?, ?)", (account_id, text))
        self.conn.commit()
        print("Post created by " + string(account_id))
        
    def add_like(self, account_id, post_id):
        self.cursor.execute("INSERT INTO Likes (account_id, post_id) VALUES (?, ?)", (account_id, post_id))
        self.conn.commit()
        print(string(account_id) + " liked the post " string(post_id))
        
    def create_mute(self, muter_id, muted_id):
        self.cursor.execute("INSERT INTO Mutes (muter_id, muting_id) VALUES (?, ?)", (muter_id, muted_id)
        self.conn.commit()
        print(string(muter_id) + " muted " string(muted_id))
        
    def create_follow(self, follower_id, followed_id):
        self.cursor.execute("INSERT INTO Followers (follower_id, following_id) VALUES (?, ?)", (follower_id, followed_id)
        self.conn.commit()
        print(string(follower_id) + " followed " + string(followed_id)

    def list_users(self):
        self.cursor.execute("SELECT * FROM Users")
        users = self.cursor.fetchall()
        for user in users:
            print(user)

    def list_accounts(self):
        self.cursor.execute("SELECT * FROM Accounts")
        accounts = self.cursor.fetchall()
        for account in accounts:
            print(account)

    def close(self):
        self.conn.close()