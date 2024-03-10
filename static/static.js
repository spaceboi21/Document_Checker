const form = document.querySelector('form');

// Make upload boxes clickable
document.addEventListener('click', function(event) {
  const clickedElement = event.target;
  if (clickedElement.classList.contains('upload-box')) {
    clickedElement.querySelector('input[type="file"]').click();
  }
});

// Display selected filenames
form.addEventListener('change', function(event) {
  const clickedElement = event.target;
  if (clickedElement.tagName === 'INPUT' && clickedElement.type === 'file') {
    const label = clickedElement.parentElement.querySelector('h3');
    const filename = clickedElement.value.split('\\').pop();
    label.textContent = filename || 'No file chosen';
  }
});

// Handle form submission
form.addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission
  
    const formData = new FormData(this); // 'this' refers to the form itself
  
    try {
      // Send data using an AJAX call - example using fetch API
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      // Handle the response from your Flask app.
      const data = await response.text();
  
      const resultsDiv = document.querySelector('.result');
      resultsDiv.innerHTML = data; // Assuming Flask returns HTML
    } catch (error) {
      console.error('Error:', error);
      // Handle errors (e.g., display an error message)
    }
  });
