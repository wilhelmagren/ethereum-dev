<script lang="ts">
  let loading = false;
  let listings: string[] = [];
  let errorMessage = '';

  async function fetchListings() {
    loading = true;
    errorMessage = '';
    try {
      const response = await fetch('http://localhost:8000/_api/redbank/carListings', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        listings = (await response.json()).listings;
      } else {
        errorMessage = 'Failed to fetch car listings';
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }

  // Fetch listings when the component is mounted
  fetchListings();
</script>

<h1>Your listed car sales</h1>

{#if loading}
  <div class="spinner"></div>
{/if}

{#if errorMessage}
  <div class="message-box error-message">{errorMessage}</div>
{/if}

{#if listings.length > 0}
  <ul>
    {#each listings as listing}
      <li>{listing}</li>
    {/each}
  </ul>
{:else if !loading}
  <p>No car listings found.</p>
{/if}

<nav>
    <a href="/">Home</a>
    <a href="/cars">Cars</a>
    <a href="/tokenize">Tokenize</a>
    <a href="/bluebank">BlueBank</a>
    <a href="/redbank">RedBank</a>
</nav>