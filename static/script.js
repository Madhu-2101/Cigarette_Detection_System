const socket = io();

function startVideo() {
    socket.emit('start_video');
}

function stopVideo() {
    socket.emit('stop_video');
}

socket.on('video_started', function(data) {
    console.log(data.message);
});

socket.on('video_stopped', function(data) {
    console.log(data.message);
});

// setInterval(() => {
//     window.location.reload(); // Reload the current page
// }, 2000);

let refreshInterval = null;

// Listen for the 'camera_status' event from the backend
socket.on('camera_status', (data) => {
    console.log('Received camera_status event:', data);
    if (data.status === 'on') {
        console.log('Camera is on. Starting interval.');
        // Start the interval when the camera is on
        refreshInterval = setInterval(() => {
            window.location.reload(); // Reload the current page
        }, 2000);
    } else if (data.status === 'off') {
        console.log('Camera is off. Stopping interval.');
        // Stop the interval when the camera is off
        if (refreshInterval) {
            clearInterval(refreshInterval);
            refreshInterval = null;
        }
    }
});
