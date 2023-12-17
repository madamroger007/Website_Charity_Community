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
            delete_news(usersId)
            Swal.fire("Hapus!", "", "success");

        } else if (result.isDenied) {
            Swal.fire("Tidak Bisa dihapus", "", "info");
        }
    });
}

function UpdateSweetAlert(usersId) {
    Swal.fire({
        title: "Apakah yakin memperbarui data?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Edit",

    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            update_news(usersId)
            Swal.fire("Perubahan di simpan!", "", "success");

        } else if (result.isDenied) {
            Swal.fire("Tidak bisa di edit", "", "info");
        }
    });
}
// iMage


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



$(document).ready(function () {
    get_news("")

});
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');




//*******************************************  Post Function
function submitNews() {
    let formData = new FormData($("#newsForm")[0]);
    console.log(formData)
    $.ajax({
        type: "POST",
        url: "/posting_news",
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response);
            // Handle the response as needed, e.g., show success message or redirect
            window.location.reload()
        },
        error: function (error) {
            console.error(error);
        }
    });
}

//*******************************************  Get function
function get_news(topic) {
    $.ajax({
        type: 'GET',
        url: "/get_news",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            const memo = topic == "" ? response.news : response.news.filter(article => article.topic === topic);
            

            console.log(memo)
            getComponentTopicNews(memo)


        },
        error: function (error) {
            console.error(error);
        }
    });
}


//******************************************* Update Function
function showUpdateCard(newsId) {
    $.ajax({
        type: 'GET',
        url: "/get_news/" + newsId,
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            console.log("cek");

            ShowUpdateComponent(response.news)

        }
    });
}



function update_news(newsId) {
    let formData = new FormData($("#updateForm")[0]);
  
    $.ajax({
        type: "POST",
        url: "/update_news/" + newsId,
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response);
            // Handle the response as needed, e.g., show success message or redirect
            ToastJs("success", "Berhasil memperbarui")
            setTimeout(function () {
                console.log("Waktu telah berlalu setelah 2 detik!");
                window.location.reload()
            }, 5000);
        },
        error: function (error) {
            console.error(error);
        }
    });
}

//******************************************* Delete Function

function delete_news(newsId) {
    console.log(newsId)
    $.ajax({
        type: 'POST',
        url: "/delete_news/" + newsId,
        headers: {
            'X-CSRFToken': csrfToken  // Setel token CSRF di header
        },
        success: function (response) {
            // Handle success, e.g., update the UI or reload the page
            console.log(response);
            ToastJs("success", "Berhasil di hapus")
            setTimeout(function () {
                console.log("Waktu telah berlalu setelah 2 detik!");
                window.location.reload()
            }, 5000);

        },
        error: function (error) {
            // Handle error, e.g., show an alert
            console.error(error);
        }
    })
}



//******************************************* Component

function ShowUpdateComponent(news) {
    $('#modal-edit').addClass('is-active');
    const { _id, title, username, img, topic, description, date } = news;
    let modalContent = `
    <div class="modal-background">
    </div>
            
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title">Update News</p>
                    <button class="delete" aria-label="close"
                        onclick="$('#modal-edit').removeClass('is-active')"></button>
                </header>
                <section class="modal-card-body text-start">
                <div class="field">
                    <label for="input-name" >Title</label>
                    <p class="control">
                        <input type="text" name="title_update" id="title_update"
                            class="input" placeholder="Input your name"
                            value="${title}">
                    </p>
                </div>


                <!-- Img... -->
                <figure class="image is-128x128 mx-auto">
                  <img src="/static/${img}" id='image-preview-card'  style="width: 150px; height: 150px;">
                </figure>
                <!-- End Img... -->
                

                <div class="field">
                    <label for="input-pic" >Update News</label>
                    <div class="control is-expanded">
                        <div class="file has-name">
                            <label class="file-label" style="width: 100%;">
                                <input name="img_update" id="imageInput"
                                    class="file-input" type="file" onchange='showImage()'>
                                <span class="file-cta">
                                    <span class="file-icon">
                                        <i class="fa fa-upload"></i>
                                    </span>
                                    <span class="file-label">Select a file</span>
                                </span>
                                <span id="file-name" class="file-name"
                                    style="width: 100%; max-width:100%;">
                                    ${img}
                                </span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="field">
                    <label for="textarea-about" >Description</label>
                    <p class="control">
                        <textarea id="description_update" name="description_update"
                            class="textarea" placeholder="pleace introduce yourself"
                            value="${description}">${description}</textarea>
                    </p>
                </div>


                <div class="field">
                <label >Topic</label>
                <div class="control">
                  <div class="select">
                  <select name="topic_update" id="topic_update">

                  <option value="">Select a topic</option>

                  <option value="sosial" ${topic === "sosial" ? "selected" : ""}>
                      Sosial</option>
                  <option value="bencana" ${topic === "bencana" ? "selected" : ""}>
                      Bencana</option>
                  <option value="konflik" ${topic === "konflik" ? "selected" : ""}>
                      Konflik</option>
              </select>
                  </div>
                </div>
              </div>

               
              
            </section>
            <footer class="modal-card-foot">
                <button type="button" class="button is-success"
                    onclick="UpdateSweetAlert('${_id}')" type='button'>Update</button>
                <button class="button"
                    onclick="$('#modal-edit').removeClass('is-active')">Cancel</button>
            </footer>
            </div>     

`;

    // Hapus konten modal sebelumnya dan tambahkan yang baru
    $('#modal-edit').empty().append(modalContent);
}



function FormNewsPost() {
    $('#modal-news-card').addClass('is-active');

    let modalContent = `

    <div class="modal-background">
    </div>
        <div class="modal-card">
             
<header class="modal-card-head">
<p class="modal-card-title">Posting News</p>
<button class="delete" aria-label="close"  onclick="$('#modal-news-card').removeClass('is-active')"></button>
</header>
<section class="modal-card-body text-start">


<!-- Input title... -->
<div class="field">
  <label >Title news</label>
  <div class="control has-icons-left has-icons-right">
    <input class="input " type="text" placeholder="Text input" name="title_give" required>
    <span class="icon is-small is-left">
    <i class="fa-solid fa-book"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-check"></i>
    </span>
  </div>
  <p class="help ">This Title News</p>
</div>
<!--End Input fb ... -->



<!-- Img... -->
<figure class="image is-128x128 mx-auto">
  <img src="https://bulma.io/images/placeholders/1280x960.png" id='image-preview-card'  style="width: 150px; height: 150px;">
</figure>
<!-- End Img... -->

<!-- Content ... -->

<div class="field">
<label for="input-pic" >Img</label>
<div class="control is-expanded">
<div class="file has-name">
<label class="file-label" style="width: 100%;">
<input name="img_give" id="imageInput" class="file-input" type="file" onchange="showImage()" required>
<span class="file-cta">
<span class="file-icon">
<i class="fa fa-upload"></i>
</span>
<span class="file-label " >Select a file</span>
</span>
<span id="file-name" class="file-name" style="width: 100%; max-width:100%;">
</span>
</label>
</div>
</div>
</div>
<!--End Content ... -->



<!-- Input Desc ... -->
<div class="field">
  <label >Description</label>
  <div class="control has-icons-left has-icons-right">
 
    <textarea class="textarea " placeholder="Text input" name="description_give" required></textarea>
    <span class="icon is-small is-left">
    <i class="fa-solid fa-arrow-down-z-a"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-check"></i>
    </span>
  </div>
  <p class="help ">This Description News</p>
</div>
<!--End Input Desc ... -->

<!-- Drop topic ... -->
<div class="select">
  <select name="topic_give" id="topic" required>
    <option value="">Select Topic</option>
    <option value="sosial">Sosial</option>
    <option value="bencana">Bencana</option>
    <option value="konflik">Konflik</option>

  </select>
</div>
<!--End Input yt ... -->



</section>
<footer class="modal-card-foot">
<button type="button" class="button is-success" onclick="submitNews()">Posting</button>
<button class="button" onclick="$('#modal-news-card').removeClass('is-active')">Cancel</button>
</footer>   
    </div>


    `;

    $('#modal-news-card').empty().append(modalContent)
}


function getComponentTopicNews(news) {
    $("#newscard-container").empty()

    for (let index = 0; index < news.length; index++) {
        let topic = news[index];
        
        let load =`
        <div class='wrapper-news  d-flex justify-content-center align-items-center' id="load-card">
        <div class="loader-img " ></div> 
        </div>
        `
        let temp = `
    
    <div class="wrap-news normal-news">
    <div class="wrapper-news">
       
        <header class="container-fluid-news">
            <figure class="figure-news"><img
                    src="/static/${topic.img}">
            </figure>
            <div class="tag-news">${topic.topic.toUpperCase()}</div>
        </header>
        <article class="content-news">
            <h1>${topic.title}</h1>
          
            <p>${topic.description}</p>
            <footer class='d-flex'>
                <span class='flex-grow-1'>&#9900; ${moment(topic.date).fromNow()}</span>
        
                <div class="dropdown">
  <div class="btn" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
  <i class="mdi mdi-dots-vertical fw-bold fs-3"></i>
  </div>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item" onclick="showUpdateCard('${topic._id}')" ><i class="mdi mdi-border-color fw-bold" style="font-size: medium;"></i> Update</a></li>
    <li><a class="dropdown-item" onclick="DeleteSweetAlert('${topic._id}')" ><i class='mdi mdi-delete-forever'> </i> Delete</a></li>
 
  </ul>
</div>
            </footer>
        </article>
    </div>

</div>  
    
    `

    $("#newscard-container").append(load)
    setTimeout(function () {
        console.log("Waktu telah berlalu setelah 2 detik!");
        $("#load-card").remove();
        $("#newscard-container").append(temp)
    }, 2000);

  
    }

}


