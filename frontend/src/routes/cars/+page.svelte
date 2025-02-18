<script lang="ts">
  let uniqueId = '';
  let loading = false;
  let responseData: any = null;
  let errorMessage = '';

  async function handleSubmit() {
    loading = true;
    responseData = null;
    errorMessage = '';
    try {
      const response = await fetch(`http://localhost:8000/_api/cars/${uniqueId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        responseData = await response.json();
      } else {
        errorMessage = 'Failed to fetch car details: ' + (await response.json()).message;
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }
</script>

<h1>Fetch Car Details</h1>

<form on:submit|preventDefault={handleSubmit}>
  <label for="uniqueId">Unique ID</label>
  <input type="text" id="uniqueId" bind:value={uniqueId} required>

  <button type="submit" disabled={loading}>Submit</button>
</form>

{#if loading}
  <div class="spinner"></div>
{/if}

{#if responseData}
<div class="response-box">
  <table>
    <thead>
      <tr>
        <th>Field</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {#each Object.entries(responseData) as [key, value]}
        <tr>
          <td><b>{key}</b></td>
          <td>{value}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
{/if}

{#if errorMessage}
  <div class="error-message">{errorMessage}</div>
{/if}

<nav>
    <a href="/">Home</a>
    <a href="/cars">Cars</a>
    <a href="/tokenize">Tokenize</a>
    <a href="/bluebank">BlueBank</a>
    <a href="/redbank">RedBank</a>
</nav>