document.addEventListener('DOMContentLoaded', () => {
    const connectBtn = document.getElementById('connectWalletBtn');
    const forceBtn = document.getElementById('forceConnectBtn');
    const walletDisplay = document.getElementById('walletAddressDisplay');
    const walletHidden = document.getElementById('walletAddressInput');
    const form = document.getElementById('createPoolForm');
    const submitBtn = document.getElementById('submitBtn');
    const statusDiv = document.getElementById('formStatus');

    let currentWallet = null;

    async function connectWallet() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                currentWallet = accounts[0];
                walletHidden.value = currentWallet;
                walletDisplay.innerText = `${currentWallet.slice(0,6)}...${currentWallet.slice(-4)}`;
                showStatus('کیف پول متصل شد', 'success');
                submitBtn.disabled = false;
            } catch (err) {
                currentWallet = null;
                walletDisplay.innerText = 'اتصال ناموفق';
                showStatus('اتصال کیف پول لغو شد', 'error');
                submitBtn.disabled = true;
            }
        } else {
            alert('لطفاً متامسک یا کیف پول Web3 نصب کنید.');
            showStatus('کیف پول Web3 یافت نشد', 'error');
            submitBtn.disabled = true;
        }
    }

    if (connectBtn) connectBtn.addEventListener('click', connectWallet);
    if (forceBtn) forceBtn.addEventListener('click', connectWallet);

    if (window.ethereum && window.ethereum.selectedAddress) {
        connectWallet();
    } else {
        submitBtn.disabled = true;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentWallet) {
            showStatus('لطفاً ابتدا کیف پول خود را متصل کنید', 'error');
            return;
        }

        const token0 = document.getElementById('token0').value.trim();
        const token1 = document.getElementById('token1').value.trim();
        const initialRate = document.getElementById('initialRate').value.trim();
        const initialLiquidity = document.getElementById('initialLiquidity').value.trim();
        const symbol0 = document.getElementById('symbol0').value.trim();
        const symbol1 = document.getElementById('symbol1').value.trim();

        if (!token0 || !token1 || !initialRate) {
            showStatus('لطفاً آدرس توکن اول، دوم و نرخ اولیه را وارد کنید', 'error');
            return;
        }

        if (!/^0x[a-fA-F0-9]{40}$/.test(token0) || !/^0x[a-fA-F0-9]{40}$/.test(token1)) {
            showStatus('آدرس توکن باید معتبر و به فرمت 0x... باشد', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.innerHTML = '⏳ در حال ایجاد استخر...';

        const payload = {
            wallet_address: currentWallet,
            token0,
            token1,
            initial_rate: initialRate,
            initial_liquidity: initialLiquidity || null,
            symbol0: symbol0 || null,
            symbol1: symbol1 || null
        };

        try {
            const response = await fetch('/dex_1/api/create_pool', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (response.ok) {
                showStatus('✅ استخر نقدینگی با موفقیت ایجاد شد!', 'success');
                form.reset();
                setTimeout(() => {
                    window.location.href = '/dex_1/';
                }, 2000);
            } else {
                showStatus('❌ خطا: ' + (data.error || 'مشکل در ایجاد استخر'), 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '✅ ایجاد استخر';
            }
        } catch (err) {
            console.error(err);
            showStatus('❌ خطای شبکه. دوباره تلاش کنید.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = '✅ ایجاد استخر';
        }
    });

    function showStatus(msg, type) {
        statusDiv.innerText = msg;
        statusDiv.className = `status ${type}`;
        setTimeout(() => {
            if (statusDiv.innerText === msg) statusDiv.innerText = '';
        }, 5000);
    }
});