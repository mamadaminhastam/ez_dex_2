// dex_1/front_end/static/js/register.js
document.addEventListener('DOMContentLoaded', () => {
    const connectBtn = document.getElementById('connectWalletBtn');
    const forceBtn = document.getElementById('forceConnectBtn');
    const walletStatus = document.getElementById('walletStatus');
    const walletHidden = document.getElementById('walletAddress');
    const form = document.getElementById('registerForm');
    const submitBtn = document.getElementById('submitBtn');
    const statusDiv = document.getElementById('formStatus');
    let currentWallet = null;

    // تابع اتصال به ولت (اختیاری)
    async function connectWallet() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                currentWallet = accounts[0];
                walletHidden.value = currentWallet;
                walletStatus.innerText = `${currentWallet.slice(0,6)}...${currentWallet.slice(-4)} (متصل)`;
                showStatus('کیف پول متصل شد (اختیاری)', 'success');
            } catch (err) {
                currentWallet = null;
                walletHidden.value = '';
                walletStatus.innerText = 'اتصال ناموفق (اختیاری)';
                showStatus('اتصال کیف پول لغو شد، اما می‌توانید بدون ولت ثبت‌نام کنید', 'success');
            }
        } else {
            walletStatus.innerText = 'کیف پول نصب نیست (اختیاری)';
            showStatus('برای اتصال ولت، متامسک نصب کنید. ثبت‌نام بدون ولت امکان‌پذیر است.', 'success');
        }
    }

    // دکمه‌های اتصال ولت
    if (connectBtn) connectBtn.addEventListener('click', connectWallet);
    if (forceBtn) forceBtn.addEventListener('click', connectWallet);

    // اگر قبلاً متامسک متصل بود، اطلاعات را بگیر (اختیاری)
    if (window.ethereum && window.ethereum.selectedAddress) {
        currentWallet = window.ethereum.selectedAddress;
        walletHidden.value = currentWallet;
        walletStatus.innerText = `${currentWallet.slice(0,6)}...${currentWallet.slice(-4)} (متصل)`;
    }

    // دکمه ثبت‌نام همیشه فعال است (حتی بدون ولت)
    submitBtn.disabled = false;

    // ثبت‌نام
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const role = document.getElementById('role').value;
        
        if (!username || !email) {
            showStatus('نام کاربری و ایمیل الزامی است', 'error');
            return;
        }
        if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            showStatus('فرمت نام کاربری نامعتبر (فقط حروف انگلیسی، اعداد و زیرخط)', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.innerText = '⏳ در حال ثبت...';

        // ولت می‌تواند null باشد (اختیاری)
        const walletAddress = currentWallet || null;

        const payload = {
            wallet_address: walletAddress,
            username: username,
            email: email,
            role: role
        };

        try {
            const res = await fetch('/dex_1/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (res.ok) {
                showStatus('✅ ثبت‌نام موفق! در حال انتقال...', 'success');
                setTimeout(() => {
                    window.location.href = '/dex_1/';
                }, 1500);
            } else {
                showStatus('❌ خطا: ' + (data.error || 'ناموفق'), 'error');
                submitBtn.disabled = false;
                submitBtn.innerText = '✅ ثبت‌نام';
            }
        } catch (err) {
            console.error('Fetch error:', err);
            showStatus('❌ خطای شبکه. سرور در دسترس نیست.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerText = '✅ ثبت‌نام';
        }
    });

    function showStatus(msg, type) {
        statusDiv.innerText = msg;
        statusDiv.className = `status ${type}`;
        setTimeout(() => {
            if (statusDiv.innerText === msg) statusDiv.innerText = '';
        }, 4000);
    }
});