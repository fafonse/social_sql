import sqlite3
import string
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
        print("Post created by " + str(account_id))
        
    def add_like(self, account_id, post_id):
        self.cursor.execute("INSERT INTO Likes (account_id, post_id) VALUES (?, ?)", (account_id, post_id))
        self.conn.commit()
        print(str(account_id) + " liked the post " + str(post_id))
        
    def create_mute(self, muter_id, muted_id):
        self.cursor.execute("INSERT INTO Mutes (muter_id, muting_id) VALUES (?, ?)", (muter_id, muted_id))
        self.conn.commit()
        print(str(muter_id) + " muted " +str(muted_id))
        
    def create_follow(self, follower_id, followed_id):
        self.cursor.execute("INSERT INTO Followers (follower_id, following_id) VALUES (?, ?)", (follower_id, followed_id))
        self.conn.commit()
        print(str(follower_id) + " followed " + str(followed_id))

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

    def get_user_feed(self, username):
        # First, find the user_id based on the username
        self.cursor.execute('''
            SELECT id FROM Accounts WHERE username = ?
        ''', (username,))
        user_account = self.cursor.fetchone()
        
        if user_account is None:
            print(f"User with username '{username}' not found.")
            return []

        user_id = user_account[0]

        # Fetch the posts from people the user is following and sort by likes, excluding muted users
        self.cursor.execute('''
            WITH Following AS (
                -- Find who the user is following
                SELECT following_id 
                FROM Followers
                WHERE follower_id = ?
            ), Muted AS (
                -- Find muted accounts by the user
                SELECT muting_id
                FROM Mutes
                WHERE muter_id = ?
            )
            SELECT p.id, p.account_id, p.content, p.timestamp, COUNT(l.id) AS like_count
            FROM Posts p
            JOIN Likes l ON p.id = l.post_id
            WHERE p.account_id IN (SELECT following_id FROM Following)
            AND p.account_id NOT IN (SELECT muting_id FROM Muted)
            GROUP BY p.id
            ORDER BY like_count DESC, p.timestamp DESC
        ''', (user_id, user_id))

        posts = self.cursor.fetchall()

        # Display the feed (post content with like count)
        for post in posts:
            post_id, account_id, content, timestamp, like_count = post
            self.cursor.execute('''
                SELECT username FROM Accounts WHERE id = ?
            ''', (account_id,))
            username = self.cursor.fetchone()[0]

            print(f"Post by {username} at ({timestamp}) reading: {content}")
            print(f"With like count: {like_count}\n")
    
    def close(self):
        self.conn.close()
    
    def print_bacon_like_numbers(self, username,maxNum):
        db_path = "social.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # likes [(1, 'alice456', 1), (2, 'charlie789', 2), (3, 'david000', 3), (4, 'eve999', 4)]

        # posts [(1, 'bob123', '1', '2025-02-21 20:39:35'), (2, 'alice456', '2', '2025-02-21 20:39:35'), (3, 'charlie789', '3', '2025-02-21 20:39:35'), (4, 'david000', '4', '2025-02-21 20:39:35')]
       
        cursor.execute('''
                 WITH RECURSIVE base AS (
                  -- Base case: Start with the given username's account ID
                SELECT a.id AS account_id, a.username as name, 0 AS like_number
                FROM Accounts a
                WHERE a.username = ? 

                UNION ALL

                -- Recursive case: Find accounts whose posts were liked by the previous level
                SELECT DISTINCT a.id, a.username, b.like_number + 1
                FROM base b
                JOIN Posts p ON p.account_id = b.account_id  -- Get the posts of the previous level accounts
                JOIN Likes l ON l.post_id = p.id  -- Get the likes for those posts
                JOIN Accounts a ON a.id = l.account_id  -- Get the accounts that liked those posts
                WHERE b.like_number <= ?  -- Optional depth limit
            )
            SELECT a.username, base.like_number  -- Only select the username and like_number
            FROM base
            JOIN Accounts a ON a.id = base.account_id
            GROUP BY a.username
            ORDER BY base.like_number, a.username;
        ''', (username,maxNum,))

        results = cursor.fetchall()
        print(f"From account named: " + username + ", With max like number of: " + str(maxNum))
        for row in results:
            print(f"Username: {row[0]}, Like Number: {row[1]}")
        #print(len(results))