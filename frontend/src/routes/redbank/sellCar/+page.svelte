<script lang="ts">
  let tokenizedAddress = '';
  let buyerAddress = '';
  let sellerAddress = '';
  let price: number | null = null;
  let lastPurchaseDate = '';
  let loading = false;
  let successMessage = '';
  let errorMessage = '';

  async function handleSubmit() {
    loading = true;
    successMessage = '';
    errorMessage = '';
    try {
      const response = await fetch('http://localhost:8000/_api/redbank/listCarForSale', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tokenizedAddress, price, lastPurchaseDate, buyerAddress, sellerAddress })
      });

      if (response.ok) {
        successMessage = 'Car listing created successfully!';
      } else {
        errorMessage = 'Failed to create car listing';
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }
</script>

<h1>Create car sale listing</h1>

<form on:submit|preventDefault={handleSubmit}>
  <label for="tokenizedAddress">Car tokenized address</label>
  <input type="text" id="tokenizedAddress" bind:value={tokenizedAddress} required>

  <label for="buyerAddress">Buyer address</label>
  <input type="text" id="buyerAddress" bind:value={buyerAddress} required>

  <label for="sellerAddress">Seller address</label>
  <input type="text" id="sellerAddress" bind:value={sellerAddress} required>

  <label for="price">Price</label>
  <input type="text" id="price" bind:value={price} required>

  <label for="lastPurchaseDate">Last purchase date</label>
  <input type="text" id="lastPurchaseDate" bind:value={lastPurchaseDate} placeholder="YYYY-DD-MM" required>

  <button type="submit" disabled={loading}>Create Listing</button>
</form>

{#if loading}
  <div class="spinner"></div>
{/if}

{#if successMessage}
  <div class="message-box success-message">{successMessage}</div>
{/if}

{#if errorMessage}
  <div class="message-box error-message">{errorMessage}</div>
{/if}

<nav>
    <a href="/">Home</a>
    <a href="/cars">Cars</a>
    <a href="/tokenize">Tokenize</a>
    <a href="/bluebank">BlueBank</a>
    <a href="/redbank">RedBank</a>
</nav>