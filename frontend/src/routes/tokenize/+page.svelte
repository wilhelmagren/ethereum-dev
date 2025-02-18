<h1>Car tokenization service</h1>

<form on:submit|preventDefault={handleSubmit}>
  <label for="modelName">Model name</label>
  <input type="text" id="modelName" bind:value={modelName} required>

  <label for="licensePlate">License plate</label>
  <input type="text" id="licensePlate" bind:value={licensePlate} required>

  <label for="manufacturedDate">Manufactured date</label>
  <input type="text" id="manufacturedDate" bind:value={manufacturedDate} placeholder="YYYY-MM-DD" required>

  <label for="uniqueId">Unique ID</label>
  <input type="text" id="uniqueId" bind:value={uniqueId} required>

  <label for="owner">Owner (wallet address)</label>
  <input type="text" id="owner" bind:value={owner} required>

  <button type="submit" disabled={loading}>Submit</button>
</form>

{#if loading}
  <div class="spinner"></div>
{/if}

{#if successMessage}
  <div class="message-box success-message">{successMessage}</div>
{/if}

{#if errorMessage}
  <div class="message-box failed-message">{errorMessage}</div>
{/if}

<nav>
    <a href="/">Home</a>
    <a href="/cars">Cars</a>
    <a href="/tokenize">Tokenize</a>
    <a href="/bluebank">BlueBank</a>
    <a href="/redbank">RedBank</a>
</nav>

<script lang="ts">
  let modelName = '';
  let licensePlate = '';
  let manufacturedDate = '';
  let uniqueId = '';
  let owner = '';
  let loading = false;
  let successMessage = '';
  let errorMessage = '';

  async function handleSubmit() {
    loading = true;
    successMessage = '';
    errorMessage = '';
    try {
      const response = await fetch('http://localhost:8000/_api/tokenize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          modelName,
          licensePlate,
          manufacturedDate,
          uniqueId,
          owner
        })
      });

      const responseData = await response.json();

      if (response.ok) {
        successMessage = responseData.message || 'Car tokenized successfully!';
        console.log('Data submitted successfully');
      } else {
        errorMessage = responseData.message || 'Failed to tokenize car';
        console.error('Failed to submit data');
      }
    } catch (error) {
      errorMessage = 'Failed to submit data: ' + error;
      console.error('Error:', error);
    } finally {
      loading = false;
    }
  }
</script>