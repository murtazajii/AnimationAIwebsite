
document.addEventListener('DOMContentLoaded', function() {
    const createVideoButton = document.getElementById('createVideoButton');
    if (createVideoButton) {
        createVideoButton.addEventListener('click', function() {
            // Gather file inputs
            const videoTemplate = document.getElementById('videoTemplate').files[0];
            const characterImages = document.getElementById('characterImages').files;
            const musicFile = document.getElementById('musicFile').files[0];

            // Create FormData object and append files
            const formData = new FormData();
            formData.append('videoTemplate', videoTemplate);
            for (let i = 0; i < characterImages.length; i++) {
                formData.append('characterImages', characterImages[i]);
            }
            formData.append('musicFile', musicFile);

            // Send AJAX request to Flask server
            const xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://127.0.0.1:5000/create_video'); // Flask route URL
            xhr.onload = function() {
                if (xhr.status === 200) {
                    // On success, display the generated video
                    const videoURL = URL.createObjectURL(xhr.response);
                    const videoPreview = document.getElementById('videoPreview');
                    videoPreview.src = videoURL;
                    videoPreview.style.display = 'block';

                    // Show download link for the generated video
                    const downloadLink = document.getElementById('downloadLink');
                    downloadLink.href = videoURL;
                    downloadLink.style.display = 'block';
                } else {
                    console.error('Error creating video:', xhr.statusText);
                }
            };
            xhr.onerror = function() {
                console.error('Error creating video:', xhr.statusText);
            };
            xhr.responseType = 'blob';
            xhr.send(formData);
        });
    } else {
        console.error('Element with ID "createVideoButton" not found.');
    }
});
