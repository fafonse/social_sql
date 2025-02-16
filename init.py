from queries import SocialNetwork


social = SocialNetwork()

try:
    social.create_user("bob@example.com")
    social.create_user("bobert@example.com")


    social.create_account("bob@example.com", "bob123")
    social.create_account("bobert@example.com", "bobert123")
    social.create_account("bobert@example.com", "alterBober")


    print("Users:")
    social.list_users()

    print("\nAccounts:")
    social.list_accounts()

    social.close()
except Exception as e:
    raise e