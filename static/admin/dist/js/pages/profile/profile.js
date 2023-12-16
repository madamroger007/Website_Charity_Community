//  Documen ready
$(document).ready(function () {
    $("#update-btn").click(function () {
        // Panggil fungsi showUpdateUsers dengan meneruskan data JSON
        showUpdateUsers(data);
    });
});


const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


function update_users(usersId) {
    let formData = new FormData($("#UsersupdateForms")[0]);
    console.log(formData)
    $.ajax({
        type: "POST",
        url: "/update_users/" + usersId,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response);
            // Handle the response as needed, e.g., show success message or redirect
            ToastJs("success","Update is success")
            setTimeout(function() {
                console.log("Waktu telah berlalu setelah 2 detik!");
                window.location.reload()
            }, 3000);
        },
        error: function (response) {
            console.log(response.errors);
        }
    });
}

function showImage() {
  const fileInput = document.getElementById('imageInput');
  const previewImg = document.getElementById('image-preview-card');

  // Pastikan file yang dipilih ada
  if (fileInput.files.length > 0) {
      // Menggunakan URL.createObjectURL untuk membuat URL sementara dari file
      const imageURL = URL.createObjectURL(fileInput.files[0]);

      // Menetapkan URL sebagai src untuk elemen gambar
      previewImg.src = imageURL;
  }
}


function showUpdateUsers(users) {
    $('#modal-edit').addClass('is-active');

    console.log(users._id)
    let modalContent = `
    <div class="modal-background">
    </div>
        <div class="modal-card">
             
<header class="modal-card-head">
<p class="modal-card-title">Update Profile Identity</p>
<button class="delete" aria-label="close"  onclick="$('#modal-edit').removeClass('is-active')"></button>
</header>
<section class="modal-card-body text-start">


<!-- Img... -->
<figure class="image is-128x128 mx-auto">
  <img src="/static/${users.profile_img}" class="is-rounded shadow-lg" id='image-preview-card' style="width: 150px; height: 150px;">
</figure>
<!-- End Img... -->

<!-- Content ... -->

<div class="field">
<label for="input-pic" class="label">Profile Picture</label>
<div class="control is-expanded">
<div class="file has-name">
<label class="file-label" style="width: 100%;">
<input name="profile_img_receive" class="file-input" id='imageInput' type="file" onchange="showImage()">
<span class="file-cta">
<span class="file-icon">
<i class="fa fa-upload"></i>
</span>
<span class="file-label">Select a file</span>
</span>
<span id="file-name" class="file-name" style="width: 100%; max-width:100%;">
${users.profile_img}
</span>
</label>
</div>
</div>
</div>
<!--End Content ... -->

<!-- Input fb ... -->
<div class="field">
  <label class="label">Facebook</label>
  <div class="control has-icons-left has-icons-right">
    <input class="input is-success" type="text" placeholder="Text input" value="https://www.facebook.com">
    <span class="icon is-small is-left">
    <i class="fab fa-facebook-f"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-check"></i>
    </span>
  </div>
  <p class="help is-success">This link facebook is available</p>
</div>
<!--End Input fb ... -->

<!-- Input x ... -->
<div class="field">
  <label class="label">Twitter</label>
  <div class="control has-icons-left has-icons-right">
    <input class="input is-success" type="text" placeholder="Text input" value="https://twitter.com">
    <span class="icon is-small is-left">
    <i class="fab fa-twitter"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-check"></i>
    </span>
  </div>
  <p class="help is-success">This link x twitter is available</p>
</div>
<!--End Input x ... -->

<!-- Input yt ... -->
<div class="field">
  <label class="label">Youtube</label>
  <div class="control has-icons-left has-icons-right">
    <input class="input is-success" type="text" placeholder="Text input" value="https://www.youtube.com">
    <span class="icon is-small is-left">
    <i class="fab fa-youtube"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-check"></i>
    </span>
  </div>
  <p class="help is-success">This link youtube is available</p>
</div>
<!--End Input yt ... -->



</section>
<footer class="modal-card-foot">
<button class="button is-success" onclick="UpdateSweetAlert('${users._id}')">Update</button>
<button class="button" onclick="$('#modal-edit').removeClass('is-active')">Cancel</button>
</footer>   
    </div>


    `;

    // Hapus konten modal sebelumnya dan tambahkan yang baru
    $('#modal-edit').empty().append(modalContent);
}

   // penggunaan SweetAlert2

function UpdateSweetAlert(usersId){
    Swal.fire({
        title: "Do you want to save the changes?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Update",
       
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          Swal.fire("Update Saved!", "", "success");
          update_users(usersId)
          
        } else if (result.isDenied) {
          Swal.fire("Changes are not update", "", "info");
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
