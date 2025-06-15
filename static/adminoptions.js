

const optionIDs = ['manageuser-existing', 'manageuser-addnew',
                   'manageclassroom-existing', 'manageclassrooom-addnew'
];


document.querySelectorAll('.option-icon, .sidebar-icon').forEach(icon => {
    icon.addEventListener('click', function() {

        const sidebar_icons = ['manageuser-logo','dashboard-logo','manageclassroom-logo']

        if (sidebar_icons.includes(this.id) && icon.getAttribute('src') === icon.getAttribute('data-inactive')){
            remove_options()
        }

        optionIDs.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = 'none';
        });

        if(this.id === 'manage-existing-user-logo'){
            document.getElementById('manageuser-existing').style.display = 'block';
        } else if (this.id === 'add-new-user-logo'){
                document.getElementById('manageuser-addnew').style.display = 'block';
        } else if (this.id === 'add-new-class-logo'){
                document.getElementById('manageclassrooom-addnew').style.display = 'block';
        }
        else if (this.id === 'manage-existing-class-logo'){
                document.getElementById('manageclassroom-existing').style.display = 'block';
        } 



    })
        
});


function remove_options(){
    optionIDs.forEach(id => {
        const el = document.getElementById(id);
        if (el){
            document.getElementById(id).style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    remove_options()
});
