$(document).ready(function(){
    getTotal()

    getNews() 
})

//********************* GET TOTAL
// Get total
function getTotal() {
    $.ajax({
        type: 'GET',
        url: "/get_total",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            TotalDonate(response);       
        },
        error: function (error) {
            console.error(error);
        }
    });

}

function TotalDonate(total){
    console.log(total.total_donation)
    $("#total-donate").text(toRupiah(total.total_donation, {useUnit: true, longUnit: true, spaceBeforeUnit: true, formal: false}))
}

//********************* Get News
// Get News
function getNews() {
    $.ajax({
        type: 'GET',
        url: "/get_news",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
        
            getCardNews(response.news)
            getFooterNews(response.news)

        },
        error: function (error) {
            console.error(error);
        }
    });

}





function getCardNews(news) {
    $("#news-card-box").empty()
    console.log(news)
    if(news.length <=3 ){
        for (let index = 0; index < news.length ; index++) {
            let berita = news[index];
            
            let load =`
            <div class='col-lg-4 col-md-6 mb-4 m-1 card-news d-flex justify-content-center align-items-center' id="load-card" style='height:400px;'>
            <div class="loader-img " ></div> 
            </div>
            `
            let temp = `
            <a href='/detail/${berita._id}' class="col-lg-4 col-md-6 card-news">
            <div class="serv-cove rounded bg-white ">
              <img src="/static/${berita.img}" alt="" class='img-news '/>
              <div class="p-2">
                <h5 class="mt-3 fs-7 fw-bold ">
                 ${berita.title}
                </h5>
                <p class='description'>${berita.description}</p>
                <span class="fs-8">${moment(berita.date).fromNow()}</span>
                <span class="float-end fs-8"><i class="bi bi-person"></i> ${berita.username}</span>
              </div>
            </div>
          </a>
        
        `
        console.log(berita);
        $("#news-card-box").append(load)
        setTimeout(function () {
           
            $("#load-card").remove();
            $("#news-card-box").append(temp)
        }, 5000);
    
      
        }

    }else{
        console.log("melebihi angka 3")
    }
 
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