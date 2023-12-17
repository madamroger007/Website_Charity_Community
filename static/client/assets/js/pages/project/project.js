$(document).ready(function(){
    getProject() 
    getNews()
  })

//********************* GET TOTAL



//********************* Get News
// Get News
function getProject() {
    $.ajax({
        type: 'GET',
        url: "/get_project",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            getCardNews(response.projects)
          },
          error: function (error) {
              console.error(error);
          }
      });
  
  }
  
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

function getCardNews(news){
    $("#card-project-container").empty()

    for (let index = 0; index < news.length; index++) {
        let berita = news[index];
        let load =`
        <div class='card-news d-flex justify-content-center align-items-center' id="load-card" style='height:400px;'>
        <div class="loader-img " ></div> 
        </div>
        `
         let temp = `
    <div class="col-lg-4 col-md-6 card-news ">
    <div class="serv-cove rounded bg-white ">
      <img src="/static/${berita.img}" alt="" class='img-news '/>
      <div class="p-2">
        <h5 class="mt-3 fs-7 fw-bold">
          ${berita.title}
        </h5>
        <p class='description'> ${berita.title}</p>
        <span class="fs-8">22 May 2015</span>
        <span class="float-end fs-8"
          ><i class="bi bi-person"></i> ${berita.username}</span
        >
      </div>
    </div>
  </div>
    `
    $("#card-project-container").append(load)
    setTimeout(function () {
        console.log("Waktu telah berlalu setelah 2 detik!");
        $("#load-card").remove();
        $("#card-project-container").append(temp)
    }, 5000);
}
}

function getFooterNews(news){

    $("#news-footer").empty()

    for (let index = 0; index < 3; index++) {
        let berita = news[index];
        
        let load =`
        <div class='post-row d-flex justify-content-center align-items-center' id="load-card" style='width: 70px;
        height: 70px;'>
        <div class="loader-img " ></div> 
        </div>
        `
        let temp = `
        <div class="post-row rounded-3">
        <div class="image">
          <img src="/static/${berita.img}"  alt="" />
        </div>
        <div class="detail">
          <p>${berita.title}</p>
        </div>
      </div>
    
    `

    $("#news-footer").append(load)
    setTimeout(function () {
        console.log("Waktu telah berlalu setelah 2 detik!");
        $("#load-card").remove();
        $("#news-footer").append(temp)
    }, 5000);

    }

}

