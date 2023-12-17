// Dapatkan token CSRF dari formulir
const csrfToken = $('meta[name=csrf-token]').attr('content');


// penggunaan SweetAlert2

   function DeleteSweter(id){
    Swal.fire({
        title: "Do you want Delete this message?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Delete",
       
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          Swal.fire("Delete!", "", "success");
          delete_msg(id)
          
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
  


$(document).ready(function () {
    updateTable()

});

function updateTable() {
    // Ambil data pengguna baru dan perbarui tabel
    $.ajax({
        type: 'GET',
        url: "/get_contact",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            console.log(response.contacs)
            updateTableContent(response.contacs);
        },
        error: function (error) {
            console.error(error);
        }
    });
}

function updateTableContent(msgs) {
    // Hapus semua baris tabel kecuali header
 
        console.log("Fungsi ini dijalankan setelah 2 detik");
        $('#msg-form').empty();

        // Tambahkan data pengguna baru ke tabel
        for (let index = 0; index < msgs.length; index++) {
            let msg = msgs[index];
            let load =`
            <div class='notification d-flex justify-content-center align-items-center' id="load-card">
            <article class="media">
            
            <div class="loader-time"></div>
            </article>
            </div>
            `


            let temp = `
            
            <div class="notification ">
            <article class="media">
                <figure class="media-left">
                  <p class="image is-64x64">
                    <img src="/static/${msg.img}">
                  </p>
                </figure>
                <div class="media-content">
                  <div class="content">
                    <p>
                      <strong>${msg.name}</strong> <small>@${msg.username}</small>  <small>${moment(msg.date).fromNow()}</small> 
                      <br>
                      ${msg.message}
                    </p>
                  </div>
                  <small><i class="fa-regular fa-envelope" style="--fa-primary-color: #ffffff; --fa-secondary-color: #ffffff;"></i>   ${msg.email}</small>
                  <nav class="level is-mobile mt-1">
                    <div class="level-left">
                      <a class="level-item" onclick="DeleteSweter('${msg._id}')">
                        <span class="icon is-small"><i class="fas fa-trash"  style="--fa-primary-color: #ffffff; --fa-secondary-color: #ffffff;"></i></span>
                      </a>

                      <div class="level-item">
                      <span class="icon is-small"><i class="fa-solid fa-check-double" style="color: #77767b;"></i></span>
                    </div>
                    </div>
                  </nav>
                </div>
                <div class="media-right">
                  <button type='button' class="delete" onclick="DeleteSweter('${msg._id}')"></button>
                </div>
              </article>
        </div>

            
            `;
            $("#msg-form").append(load)
            setTimeout(function () {
                console.log("Waktu telah berlalu setelah 2 detik!");
                $("#load-card").remove();
                $("#msg-form").append(temp)
            }, 2000);
        }
  
   
}


function delete_msg(userId) {
    $.ajax({
        type: 'POST',
        url: "/delete_contact/" + userId,
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
