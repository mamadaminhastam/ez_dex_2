# view_users.py
import sqlite3

DB = "ezdex.db"


def list_users():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, role FROM users ORDER BY id")
    users = cur.fetchall()
    conn.close()

    print("\n👥 User List")
    print("-" * 60)
    if not users:
        print("No users found.")
    else:
        for u in users:
            print(
                f"ID:{u['id']:<3} | {u['username']:<15} | {u['email']:<20} | Role: {u['role']}")
    print("-" * 60)


def change_role(user_id, new_role):
    valid_roles = ['user', 'trader', 'liquidity_provider', 'admin']
    if new_role not in valid_roles:
        print(f"Invalid role. Allowed: {valid_roles}")
        return
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    if cur.rowcount == 0:
        print("User not found.")
    else:
        conn.commit()
        print(f"✅ User {user_id} role changed to '{new_role}'.")
    conn.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        list_users()
    elif len(sys.argv) == 3 and sys.argv[1] == "role":
        try:
            uid = int(sys.argv[2])
        except ValueError:
            print("User ID must be an integer.")
            sys.exit(1)
        new_role = input(
            "New role (user/trader/liquidity_provider/admin): ").strip()
        change_role(uid, new_role)
    else:
        print("Usage:")
        print("  python view_users.py            → list all users")
        print("  python view_users.py role <id>  → change role of user")
