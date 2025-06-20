document.addEventListener('DOMContentLoaded', function() {
    const profileIcon = document.getElementById('profile-logo');
    const profilePopover = document.getElementById('profile-popover');
    const accountSettingsPopover = document.getElementById('account-settings-popover');
    const accountSettingsBtn = document.getElementById('account-settings-btn');
    const closeAccountSettingsBtn = document.getElementById('close-account-settings');
    const backToProfileBtn = document.getElementById('back-to-profile-btn');
    const changeDpBtn = document.getElementById('change-dp-btn');

    // Modal elements for profile upload
    const profileUploadModal = document.getElementById('profile-upload-modal');
    const closeProfileUploadModal = document.getElementById('close-profile-upload-modal');
    const cancelProfileUpload = document.getElementById('cancel-profile-upload');
    const profileUploadForm = document.getElementById('profile-upload-form');
    const profileUpload = document.getElementById('profile-upload');

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

    // Back to profile popover
    backToProfileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        accountSettingsPopover.style.display = 'none';
        profilePopover.style.display = 'block';
    });

    // Close account settings popover
    if (closeAccountSettingsBtn) {
        closeAccountSettingsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            accountSettingsPopover.style.display = 'none';
        });
    }

    // Show modal when "Change Display Picture" is clicked
    changeDpBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (profileUploadModal) {
            profileUploadModal.style.display = 'flex';
            if (profileUpload) profileUpload.value = ''; // reset file input
        }
    });

    // Hide modal on close or cancel
    if (closeProfileUploadModal) {
        closeProfileUploadModal.addEventListener('click', function() {
            profileUploadModal.style.display = 'none';
        });
    }
    if (cancelProfileUpload) {
        cancelProfileUpload.addEventListener('click', function() {
            profileUploadModal.style.display = 'none';
        });
    }

    // Hide modal after successful upload
    if (profileUploadForm) {
        profileUploadForm.addEventListener('submit', function() {
            profileUploadModal.style.display = 'none';
        });
    }

    // Hide modal when clicking outside modal content
    if (profileUploadModal) {
        profileUploadModal.addEventListener('click', function(e) {
            if (e.target === profileUploadModal) {
                profileUploadModal.style.display = 'none';
            }
        });
    }

    // Prevent clicks inside popovers from closing them
    profilePopover.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    accountSettingsPopover.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    // Hide popovers when clicking outside
    document.addEventListener('click', function(e) {
        if (
            !profilePopover.contains(e.target) &&
            !accountSettingsPopover.contains(e.target) &&
            e.target !== profileIcon
        ) {
            profilePopover.style.display = 'none';
            accountSettingsPopover.style.display = 'none';
        }
    });
});