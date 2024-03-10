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
form.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent default form submission

  const formData = new FormData(this); // 'this' refers to the form itself

  // Send data using an AJAX call - example using fetch API
  fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      // Handle the response from your Flask app.
      return response.text();
    })
    .then(data => {
      const resultsDiv = document.querySelector('.result');
      resultsDiv.innerHTML = data; // Assuming Flask returns HTML
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle errors (e.g., display an error message)
    });
});
