//******************************************* Libary
// penggunaan SweetAlert2
// Toast
const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    }
});
function ToastJs(icon, title) {
    Toast.fire({
        icon: icon,
        title: title
    });
}

// Delete 
const SweetDeleteButton = Swal.mixin({
    customClass: {
      confirmButton: "btn btn-danger",
      cancelButton: "btn btn-secondary"
    }
  });
function DeleteSweetAlert(usersId) {
    SweetDeleteButton.fire({
        title: "Apakah Kamu ingin menghapus?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Hapus",

    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            delete_project(usersId)
            Swal.fire("Hapus!", "", "success");

        } else if (result.isDenied) {
            Swal.fire("Tidak Bisa dihapus", "", "info");
        }
    });
}

//************************* DOM Content */
$(document).ready(function () {
    
    if(msg){
        ToastJs("warning", msg)
    }

    if(msgs){
        ToastJs("succes", msgs)
    }

});