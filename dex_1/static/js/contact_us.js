document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const statusDiv = document.getElementById('formStatus');
    const connectBtn = document.getElementById('connectWalletBtn');
    const walletInput = document.getElementById('walletAddress');

    // اتصال کیف پول Web3
    if (connectBtn) {
        connectBtn.addEventListener('click', async () => {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                    const wallet = accounts[0];
                    if (walletInput) walletInput.value = wallet;
                    showStatus(`✅ کیف پول متصل شد: ${wallet.slice(0,6)}...${wallet.slice(-4)}`, 'success');
                } catch (error) {
                    console.error(error);
                    showStatus('❌ اتصال لغو شد یا خطایی رخ داد.', 'error');
                }
            } else {
                showStatus('⚠️ لطفاً متامسک یا کیف پول Web3 نصب کنید.', 'error');
            }
        });
    }

    // ارسال فرم
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value.trim();
        const subject = document.getElementById('subject').value.trim();
        const message = document.getElementById('message').value.trim();
        const walletAddress = walletInput ? walletInput.value.trim() : '';

        if (!email || !subject || !message) {
            showStatus('لطفاً فیلدهای ایمیل، موضوع و پیام را پر کنید.', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>⏳</span> در حال ارسال...';

        const payload = {
            Email: email,
            Subject: subject,
            Message: message,
            Wallet_Address: walletAddress
        };

        try {
            const response = await fetch('dex_1/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.ok) {
                showStatus('✔️ ' + (result.message || 'پیام شما با موفقیت ثبت شد.'), 'success');
                form.reset();
            } else {
                showStatus('❌ خطا: ' + (result.error || 'مشکل در ارتباط با سرور'), 'error');
            }
        } catch (err) {
            console.error(err);
            showStatus('❌ خطای شبکه. لطفاً دوباره تلاش کنید.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>📤</span> ارسال پیام';
        }
    });

    function showStatus(msg, type) {
        statusDiv.innerHTML = msg;
        statusDiv.className = `status-message ${type}`;
        setTimeout(() => {
            if (statusDiv.innerHTML === msg) {
                statusDiv.innerHTML = '';
                statusDiv.className = 'status-message';
            }
        }, 5000);
    }
});