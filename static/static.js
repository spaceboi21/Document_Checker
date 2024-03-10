const form = document.querySelector('form');
const uploadBoxes = document.querySelectorAll('.upload-box');

// Make upload boxes clickable 
uploadBoxes.forEach(uploadBox => {
  uploadBox.addEventListener('click', function() {
    this.querySelector('input[type="file"]').click();
  });
});

// Display selected filenames
uploadBoxes.forEach(uploadBox => {
  const input = uploadBox.querySelector('input[type="file"]');
  const label = uploadBox.querySelector('h3'); 

  input.addEventListener('change', function(event) {
    const filename = this.value.split('\\').pop(); 
    label.textContent = filename || 'No file chosen';
  });
});

// Handle form submission
form.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent default form submission

  const fileInputs = document.querySelectorAll('.file-input');
  const formData = new FormData();

  fileInputs.forEach(input => {
    for (const file of input.files) {
      formData.append('files', file); // Combine files using 'files' key
    }
  });

  // Add other fields to formData
  formData.append('name', this.name.value);
  formData.append('cnic', this.cnic.value);
  formData.append('passport_number', this.passport_number.value);

  // Send data using an AJAX call - example using fetch API
  fetch('/upload', { 
    method: 'POST',
    body: formData
  })
  .then(response => {
    // Handle the response from your Flask app.
    const resultsDiv = document.querySelector('.result'); 
    resultsDiv.innerHTML = response.text(); // Assuming Flask returns HTML
  })
  .catch(error => {
    console.error('Error:', error); 
    // Handle errors (e.g., display an error message)
  });
});
