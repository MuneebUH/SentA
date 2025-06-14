document.getElementById('upload-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const preview = document.getElementById('preview');
  const charts = document.getElementById('charts');
  

  preview.innerHTML = 'Processing...';
  charts.innerHTML = '';
  sentimentTable.innerHTML = '';

  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    const text = await response.text();
    try {
      const data = JSON.parse(text);
      if (response.ok) {
        preview.innerHTML = data.preview;
        charts.innerHTML = data.chartsHtml;
        
      } else {
        alert(data.error || "Something went wrong.");
      }
    } catch (err) {
      console.error('Invalid JSON:', text);
      alert("Invalid response from server.");
    }
  } catch (error) {
    alert("Error: " + error.message);
  }
});
