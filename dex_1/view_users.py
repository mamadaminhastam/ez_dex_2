# dex_1/view_users.py
import sqlite3
import sys

DB = "dex.db"


def list_users():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, role, wallet_address FROM users ORDER BY id")
    users = cur.fetchall()
    conn.close()

    print("\n👥 User List")
    print("-" * 80)
    if not users:
        print("No users found. Please register a user first.")
    else:
        for u in users:
            print(f"ID: {u['id']:<3} | Username: {u['username']:<15} | Email: {u['email']:<20} | Role: {u['role']:<20} | Wallet: {u['wallet_address'] or 'None'}")
    print("-" * 80)


def change_role(user_id, new_role):
    valid_roles = ['user', 'trader', 'liquidity_provider', 'admin']
    if new_role not in valid_roles:
        print(f"Invalid role. Allowed roles: {valid_roles}")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    if cur.rowcount == 0:
        print(f"User with ID {user_id} not found.")
    else:
        conn.commit()
        print(f"User {user_id} role changed to '{new_role}'.")
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        list_users()
    elif len(sys.argv) == 3 and sys.argv[1] == "role":
        try:
            user_id = int(sys.argv[2])
        except ValueError:
            print("User ID must be an integer.")
            sys.exit(1)
        new_role = input(
            "New role (user/trader/liquidity_provider/admin): ").strip()
        change_role(user_id, new_role)
    else:
        print("""
Usage:
  python view_users.py               → Show all users
  python view_users.py role <id>     → Change role of a user
""")
