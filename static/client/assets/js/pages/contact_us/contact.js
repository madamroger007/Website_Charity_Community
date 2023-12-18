
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

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


function PostSweetAlert() {
    Swal.fire({
        title: "Apakah anda ingin memberikan kami pesan?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Kirim Pesan",

    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            PostContact()
            Swal.fire("Terimakasih!", "", "success");

        } else if (result.isDenied) {
            Swal.fire("Tidak bisa di Kirim", "", "info");
        }
    });
}



$(document).ready(function(){
    getNews() 
})

//********************* Get News
// Get News
function getNews() {
    $.ajax({
        type: 'GET',
        url: "/get_news",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru

            getFooterNews(response.news)

        },
        error: function (error) {
            console.error(error);
        }
    });

}

function getFooterNews(news){

    $("#news-footer").empty()
    if(news.length <=3 ){
    for (let index = 0; index < news.length; index++) {
        let berita = news[index];
        
        let load =`
        <div class='post-row d-flex justify-content-center align-items-center' id="load-card" style='width: 70px;
        height: 70px;'>
        <div class="loader-img " ></div> 
        </div>
        `
        let temp = `
        <a href='/detail/${berita._id}' class="post-row rounded-3">
        <div class="image">
          <img src="/static/${berita.img}"  alt="" />
        </div>
        <div class="detail text-white">
          <p>${berita.title}</p>
        </div>
      </a>
    
    `

    $("#news-footer").append(load)
    setTimeout(function () {
        console.log("Waktu telah berlalu setelah 2 detik!");
        $("#load-card").remove();
        $("#news-footer").append(temp)
    }, 5000);

  
    }
    }
}

function PostContact(){
    let formData = new FormData($("#FormContact")[0]);
    console.log(formData)
    $.ajax({
        type: "POST",
        url: "/posting_contact",
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response);
            setTimeout(function () {
                ToastJs("success", "Berhasil mengirim pesan")
                console.log("Waktu telah berlalu setelah 2 detik!");
               
            }, 2000);
        },
        error: function (error) {
            console.error(error);
        }
    });
}

