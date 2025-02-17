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
        errorMessage = 'Failed to fetch data';
      }
    } catch (error) {
      errorMessage = 'Error: ' + error.message;
    } finally {
      loading = false;
    }
  }
</script>

<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f5f5f7;
    color: #333;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  h1 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  form {
    max-width: 400px;
    width: 100%;
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
    box-sizing: border-box;
  }

  button {
    display: block;
    width: 100%;
    padding: 0.75rem;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #0056b3;
  }

  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #007BFF;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
    margin: 1rem auto;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .response-box {
    max-width: 400px;
    width: 100%;
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin: 1rem auto;
    word-wrap: break-word;
    overflow-wrap: break-word;
    word-break: break-all;
  }

  .error-message {
    color: red;
    text-align: center;
    margin-top: 1rem;
  }
</style>

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
    <pre>{JSON.stringify(responseData, null, 2)}</pre>
  </div>
{/if}

{#if errorMessage}
  <div class="error-message">{errorMessage}</div>
{/if}