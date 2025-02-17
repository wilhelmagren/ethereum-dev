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

  .message-box {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin: 1rem auto;
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1.25rem;
    max-width: 400px;
    width: 100%;
    word-wrap: break-word;
    overflow-wrap: break-word;
    word-break: break-all;
  }

  .success-message {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .failed-message {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #fff;
    border-top: 1px solid #ccc;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
  }

  nav a {
    color: #333;
    text-decoration: none;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  nav a:hover {
    background-color: #f0f0f5;
    color: #007BFF;
  }
</style>

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
      const response = await fetch('http://localhost:8000/tokenize', {
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