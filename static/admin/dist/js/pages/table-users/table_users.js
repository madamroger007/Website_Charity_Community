$(document).ready(function () {
    updateTable()

});

function updateTable() {
    // Ambil data pengguna baru dan perbarui tabel
    $.ajax({
        type: 'GET',
        url: "/get_users",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            console.log(response.total_users)
            updateTableContent(response.users);
        },
        error: function (error) {
            console.error(error);
        }
    });
}

function updateTableContent(users) {
    // Hapus semua baris tabel kecuali header
    setTimeout(function() {
        console.log("Fungsi ini dijalankan setelah 2 detik");
        $('#users-form').empty();

        // Tambahkan data pengguna baru ke tabel
        for (let index = 0; index < users.length; index++) {
            let user = users[index];
            let row = `
    <tr class="" style='height:50px;'>
        <th scope="row">${(index + 1)}</th>
        <td>${user.username}</td>
        <td>${user.biodata}</td>
        <td>${user.email}</td>
        <td>${user.role}</td>
        <td>${user.country}</td>
        <td>${user.phone}</td>
        <td>${user.address}</td>
        <td>
            <button class="btn" onclick='DeleteSweter("${user._id}")'><i class='mdi mdi-delete-forever'> </i></button>
        </td>
    </tr>`;
            $('#users-form').append(row);
        }
    }, 5000)
   
}


function delete_user(userId) {

    // Dapatkan token CSRF dari formulir
    let csrfToken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        type: 'POST',
        url: "/delete_user/" + userId,
        headers: {
            'X-CSRFToken': csrfToken  // Setel token CSRF di header
        },
        success: function (response) {
            // Handle success, e.g., update the UI or reload the page
            console.log(response);
            ToastJs("success","Delete is success")
            setTimeout(function() {
                console.log("Waktu telah berlalu setelah 2 detik!");
                window.location.reload()
            }, 3000);
           
        },
        error: function (error) {
            // Handle error, e.g., show an alert
            console.error(error);
        }
    })
}

   // penggunaan SweetAlert2

   function DeleteSweter(usersId){
    Swal.fire({
        title: "Do you want Delete?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Delete",
       
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          Swal.fire("Delete!", "", "success");
          delete_user(usersId)
          
        } else if (result.isDenied) {
          Swal.fire("Changes are not Delete", "", "info");
        }
      });
}

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
  function ToastJs(icon,title){
    Toast.fire({
      icon: icon,
      title: title
    });
  }
  