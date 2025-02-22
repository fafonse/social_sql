from queries import SocialNetwork
social = SocialNetwork()

try:
    # Create users
    social.create_user("bob@example.com")
    social.create_user("alice@example.com")
    social.create_user("charlie@example.com")
    social.create_user("david@example.com")
    social.create_user("eve@example.com")

    # Create accounts
    social.create_account("bob@example.com", "bob123")
    social.create_account("alice@example.com", "alice456")
    social.create_account("charlie@example.com", "charlie789")
    social.create_account("david@example.com", "david000")
    social.create_account("eve@example.com", "eve999")

    # Create posts
    social.create_post(1,"1")       # Bob's post (ID 1)
    social.create_post(2,"2")     # Alice's post (ID 2)
    social.create_post(3,"3")   # Charlie's post (ID 3)
    social.create_post(4,"4")     # David's post (ID 4)

    # Create likes
    social.add_like(2, 1)    # Alice likes Bob's post
    social.add_like(3, 2)  # Charlie likes Alice's post
    social.add_like(4, 3)    # David likes Charlie's post
    social.add_like(5, 1)      # Eve likes David's post

    # Run the like-number query
    print("\nLike Numbers:")
    social.print_bacon_like_numbers("bob123",5)
    
    social.close()
except Exception as e:
    raise e