# core/navigation.py
from core import auth


def get_nav_html(headers, current_path=""):
    user = auth.get_current_user(headers)

    nav = '<nav class="main-nav">'

    # لینک‌های همگانی
    nav += '<a href="/">🏠 Home</a>'
    nav += '<a href="/contact">📞 Contact</a>'
    nav += '<a href="/catalog">🛒 Catalog</a>'


    if user:
        # لینک‌هایی که فقط کاربران وارد‌شده می‌بینند
        nav += '<a href="/swap">💱 Swap</a>'
        nav += '<a href="/swap-history">📋 History</a>'

        # لینک‌های ویژه ادمین
        if user.get('role') == 'admin':
            nav += '<a href="/create_pool">➕ New Pool</a>'
            nav += '<a href="/admin/users">👥 Users</a>'
            nav += '<a href="/admin/pools">💧 Pools</a>'
            nav += '<a href="/admin/messages">✉️ Messages</a>'

        # نشان Admin اگر کاربر ادمین باشد
        admin_badge = ""
        if user.get('role') == 'admin':
            admin_badge = ' <span style="color: gold; font-size: 0.9rem;">👑 Admin</span>'

        # منوی کاربر با نام و نشان
        nav += '''
        <div class="user-menu">
            <div class="user-trigger">
                <span class="user-avatar">👤</span>
                <span class="username">{}{}</span>
            </div>
            <div class="dropdown-menu">
                <a href="/profile">👤 Profile</a>
                <a href="/my-pools">⭐ My Pools</a>
                <a href="/logout">🚪 Logout</a>
            </div>
        </div>
        '''.format(user["username"], admin_badge)

    else:
        # کاربر مهمان
        nav += '<a href="/register">📝 Register</a>'
        nav += '<a href="/login">🔐 Login</a>'

    nav += '</nav>'
    return nav
