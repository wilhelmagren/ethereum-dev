<script lang="ts">
  let inputString = '';
  let depositAddress = '';
  let depositAmount: number | null = null;
  let transferAddress = '';
  let transferAmount: number | null = null;
  let isDefi = false;
  let loading = false;
  let tradFiAmount: number | null = null;
  let defiAmount: number | null = null;
  let errorMessage = '';
  let successMessage = '';

  async function handleSubmit() {
    loading = true;
    tradFiAmount = null;
    defiAmount = null;
    errorMessage = '';
    successMessage = '';
    try {
      const response = await fetch(`http://localhost:8000/_api/bluebank/account/${inputString}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const responseData = await response.json();
        tradFiAmount = responseData.TradFi;
        defiAmount = responseData.DeFi;
      } else {
        errorMessage = 'Failed to fetch data';
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }

  async function handleDeposit() {
    loading = true;
    errorMessage = '';
    successMessage = '';
    try {
      const response = await fetch('http://localhost:8000/_api/bluebank/deposit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ walletAddress: depositAddress, amount: depositAmount })
      });

      if (response.ok) {
        successMessage = 'Deposit successful!';
      } else {
        errorMessage = 'Failed to deposit';
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }

  async function handleTransfer() {
    loading = true;
    errorMessage = '';
    successMessage = '';
    try {
      const response = await fetch('http://localhost:8000/_api/bluebank/transfer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ walletAddress: transferAddress, amount: transferAmount, deFi: isDefi })
      });

      if (response.ok) {
        successMessage = 'Transfer successful!';
      } else {
        errorMessage = 'Failed to transfer';
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="container">
<h1>🔵 BlueBank Account Information</h1>

<form on:submit|preventDefault={handleSubmit}>
  <label for="inputString">Enter your wallet address</label>
  <input type="text" id="inputString" bind:value={inputString} required>

  <button type="submit" disabled={loading}>Submit</button>
</form>

{#if loading}
  <div class="spinner"></div>
{/if}

{#if tradFiAmount !== null && defiAmount !== null}
  <div class="balances-container">
    <div class="balance-box">
      <h2>TradFi balance</h2>
      <p>{tradFiAmount} SEK</p>
    </div>
    <div class="balance-box">
      <h2>DeFi balance</h2>
      <p>{defiAmount} BT</p>
    </div>
  </div>
{/if}

<h2>Deposit Funds</h2>
<form on:submit|preventDefault={handleDeposit}>
  <label for="depositAddress">Enter the address to deposit to</label>
  <input type="text" id="depositAddress" bind:value={depositAddress} required>

  <label for="depositAmount">Enter the amount to deposit</label>
  <input type="number" id="depositAmount" bind:value={depositAmount} required>

  <button type="submit" disabled={loading}>Deposit</button>
</form>

<h2>Transfer Funds</h2>
<form on:submit|preventDefault={handleTransfer}>
  <label for="transferAddress">Enter your wallet address</label>
  <input type="text" id="transferAddress" bind:value={transferAddress} required>

  <label for="transferAmount">Enter the amount to transfer</label>
  <input type="number" id="transferAmount" bind:value={transferAmount} required>

  <label for="isDefi">Transfer to DeFi account?</label>
  <input type="checkbox" id="isDefi" bind:checked={isDefi}>

  <button type="submit" disabled={loading}>Transfer</button>
</form>

{#if successMessage}
  <div class="success-message">{successMessage}</div>
{/if}

{#if errorMessage}
  <div class="error-message">{errorMessage}</div>
{/if}

</div>

<nav>
    <a href="/">Home</a>
    <a href="/cars">Cars</a>
    <a href="/tokenize">Tokenize</a>
    <a href="/bluebank">BlueBank</a>
    <a href="/redbank">RedBank</a>
</nav>