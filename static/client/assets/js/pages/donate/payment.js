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
// Button klik image
$(document).ready(function () {
    $('.button-donate-value').click(function () {
        $('#image-donate').attr('src', $(this).data('src'));
        $('#donate-amount').val($(this).data('value'));
        
    });


    // Handle dropdown change event
  
});


//****************** POST function


