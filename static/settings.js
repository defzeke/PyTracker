document.addEventListener('DOMContentLoaded', function() {
    const profileIcon = document.getElementById('profile-logo');
    const profilePopover = document.getElementById('profile-popover');
    const accountSettingsPopover = document.getElementById('account-settings-popover');
    const accountSettingsBtn = document.getElementById('account-settings-btn');
    const closeAccountSettingsBtn = document.getElementById('close-account-settings');
    const changeDpBtn = document.getElementById('change-dp-btn');
    const profileUpload = document.getElementById('profile-upload');

    // Cropper modal elements
    const cropperModal = document.getElementById('cropper-modal');
    const cropperImage = document.getElementById('cropper-image');
    const cropperCancel = document.getElementById('cropper-cancel');
    const cropperSave = document.getElementById('cropper-save');
    let cropper = null;

    // Show profile popover on click
    profileIcon.addEventListener('click', function(e) {
        e.stopPropagation();
        document.querySelectorAll('.popover-panel').forEach(panel => {
            if (panel !== profilePopover) panel.style.display = 'none';
        });
        profilePopover.style.display = (profilePopover.style.display === 'block') ? 'none' : 'block';
        accountSettingsPopover.style.display = 'none';
    });

    // Show account settings popover
    accountSettingsBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        profilePopover.style.display = 'none';
        accountSettingsPopover.style.display = 'block';
    });

    // Close account settings popover
    closeAccountSettingsBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        accountSettingsPopover.style.display = 'none';
    });

    // Open file dialog when clicking "Change Display Picture"
    changeDpBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        profileUpload.click();
    });

    // Show cropper modal after file selection
    profileUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(evt) {
                cropperImage.src = evt.target.result;
                cropperModal.style.display = 'flex';
                // Wait for image to load before initializing cropper
                cropperImage.onload = function() {
                    if (cropper) cropper.destroy();
                    cropper = new Cropper(cropperImage, {
                        aspectRatio: 1, // keep it square/circle
                        viewMode: 1,
                        movable: true,
                        zoomable: true,
                        rotatable: false,
                        scalable: true,
                        cropBoxResizable: true,
                        minContainerWidth: 300,
                        minContainerHeight: 300
                    });
                };
            };
            reader.readAsDataURL(file);
        }
    });

    // Cancel cropping
    cropperCancel.addEventListener('click', function() {
        if (cropper) cropper.destroy();
        cropperModal.style.display = 'none';
        profileUpload.value = ""; // reset file input
    });

    // Save cropped image
    cropperSave.addEventListener('click', function() {
        if (cropper) {
            const canvas = cropper.getCroppedCanvas({
                width: 256,
                height: 256,
                imageSmoothingQuality: 'high'
            });
            profileIcon.src = canvas.toDataURL('image/png');
            cropper.destroy();
            cropperModal.style.display = 'none';
            profileUpload.value = ""; // reset file input
        }
    });

    // Hide popovers when clicking outside
    document.addEventListener('click', function(e) {
        if (
            !profilePopover.contains(e.target) &&
            !accountSettingsPopover.contains(e.target) &&
            e.target !== profileIcon &&
            (!cropperModal || !cropperModal.contains(e.target))
        ) {
            profilePopover.style.display = 'none';
            accountSettingsPopover.style.display = 'none';
            if (cropperModal) cropperModal.style.display = 'none';
        }
    });
});