def handle(data, user_id):
    # فقط شبیه‌سازی
    token_from = data.get('from', [''])[0]
    token_to = data.get('to', [''])[0]
    amount = data.get('amount', ['0'])[0]
    # ذخیره در تاریخچه تراکنش‌ها (جدول جدید لازم دارد)
    # می‌توان بعداً پیاده‌سازی کرد.
    return False, "امکان swap در نسخه فعلی وجود ندارد."
