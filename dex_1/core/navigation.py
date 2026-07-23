# dex_1/core/navigation.py
from core import auth


def get_nav_html(headers, current_path=""):
    user = auth.get_current_user(headers)

    nav = '<nav class="main-nav">'

    # لینک‌های همگانی (با پیشوند /dex_1)
    nav += '<a href="/dex_1/">🏠 Home</a>'
    nav += '<a href="/dex_1/contact">📞 Contact</a>'
    nav += '<a href="/dex_1/catalog">🛒 Catalog</a>'

    if user:
        nav += '<a href="/dex_1/swap">💱 Swap</a>'
        nav += '<a href="/dex_1/swap-history">📋 History</a>'

        if user.get('role') == 'admin':
            nav += '<a href="/dex_1/create_pool">➕ New Pool</a>'
            nav += '<a href="/dex_1/admin/users">👥 Users</a>'
            nav += '<a href="/dex_1/admin/pools">💧 Pools</a>'
            nav += '<a href="/dex_1/admin/messages">✉️ Messages</a>'

        admin_badge = ""
        if user.get('role') == 'admin':
            admin_badge = ' <span style="color: gold; font-size: 0.9rem;">👑 Admin</span>'

        nav += '''
        <div class="user-menu">
            <div class="user-trigger">
                <span class="user-avatar">👤</span>
                <span class="username">{}{}</span>
            </div>
            <div class="dropdown-menu">
                <a href="/dex_1/profile">👤 Profile</a>
                <a href="/dex_1/my-pools">⭐ My Pools</a>
                <a href="/dex_1/logout">🚪 Logout</a>
            </div>
        </div>
        '''.format(user["username"], admin_badge)

    else:
        nav += '<a href="/dex_1/register">📝 Register</a>'
        nav += '<a href="/dex_1/login">🔐 Login</a>'

    nav += '</nav>'
    return nav
