

document.addEventListener('DOMContentLoaded', function () {

    /* initialize the calendar
    -----------------------------------------------------------------*/

    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        editable: true,
        droppable: true, // this allows things to be dropped onto the calendar
        drop: function (arg) {
            // is the "remove after drop" checkbox checked?
            if (document.getElementById('drop-remove').checked) {
                // if so, remove the element from the "Draggable Events" list
                arg.draggedEl.parentNode.removeChild(arg.draggedEl);
            }
        }
    });
    calendar.render();
    getTotal()
    getDonate()
    getTemperature()
    getNews() 
});

// Operasion DOM Jquery

// Get total
function getTotal() {
    $.ajax({
        type: 'GET',
        url: "/get_total",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            InfoCard(response);
            

        },
        error: function (error) {
            console.error(error);
        }
    });

}

function InfoCard(total) {
    // Mengubah format tanggal dari "YYYY-MM-DD-HH-mm-ss" menjadi "DD MMMM YYYY, HH:mm:ss"
    setTimeout(function() {
        console.log("Fungsi ini dijalankan setelah 2 detik");
    
    let temp = `
    <li class="feed-item">
    <div class="feed-icon bg-info"><i class="mdi mdi-account-multiple-plus"></i></div> Total ${total.total_users} User  <span class="ms-auto font-12 text-muted">${moment(total.timestamp_users).fromNow()}</span>
</li>
<li class="feed-item">
    <div class="feed-icon bg-success"><i class="mdi mdi-currency-usd"></i></div> Total ${toRupiah(total.total_donation, { symbol: 'IDR', floatingPoint: 0 })} Donate <span class="ms-auto font-12 text-muted">${moment(total.timestamp_donations).fromNow()}</span>
</li>
<li class="feed-item">
    <div class="feed-icon bg-warning"><i class="mdi mdi-library-books"></i></div> Total ${total.total_news} News <span class="ms-auto font-12 text-muted">${moment(total.timestamp_news).fromNow()}</span>
</li>
<li class="feed-item">
    <div class="feed-icon bg-danger"><i class="mdi mdi-image-filter"></i></div> Total ${total.total_project} Project
     <span class="ms-auto font-12 text-muted">${moment(total.timestamp_projects).fromNow()}</span>
</li>
    `
    $("#information-total").empty().append(temp)
}, 5000); // Waktu diatur dalam milidetik (1000 ms = 1 detik)
}

// Get donate
function getDonate() {
    $.ajax({
        type: 'GET',
        url: "/get_donate",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
           
            updateTableDonate(response.donation)


        },
        error: function (error) {
            console.error(error);
        }
    });

}

function updateTableDonate(donation) {
    // Tambahkan data pengguna baru ke tabel
    setTimeout(function() {
        console.log("Fungsi ini dijalankan setelah 2 detik");
        $('#donation-form').empty();
        for (let index = 0; index < 10; index++) {
            let donate = donation[index];
          
            let nama = donate.username.substring(0, 2).toUpperCase();
            let row = `
            <tr class="pt-2">
            <td class="d-flex align-items-center justify-content-center"><p>${(index + 1)}</p></td>
            <td>
                <div class="d-flex align-self-start">
                    <div class="m-r-10 " style="margin-top: -10px; " >
                    <a
                    class="btn btn-circle d-flex btn-info text-white">${nama}</a>
                      
                    </div>
                    <div class="">
                        <h4 class="m-b-0 font-16">${donate.username}</h4>
                    </div>
                </div>
            </td>
            <td>${donate.email}</td>
            <td>${donate.phone}</td>
            <td>${donate.bank_account}</td>
            <td>
                <label class="label label-danger fw-bolder">${donate.country}</label>
            </td>
            <td>
            <h5 class="m-b-0">${toRupiah(donate.donation_amount, { symbol: 'IDR', floatingPoint: 0 })}</h5>
            </td>
            <td>${moment(donate.date).fromNow()}</td>
        </tr>
               
    `;
            $('#donation-form').append(row);
        }
    
    
    }, 5000); 
 
}



// Get Temperature
function getTemperature() {
    const API = "9a92556b800d4d75812121713231312"
    const city = "Jakarta"


    $.ajax({
        type: 'GET',
        url: `https://api.weatherapi.com/v1/current.json?key=${API}&q=${city}&aqi=no`,
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            Temperature(response)

        },
        error: function (error) {
            console.error(error);
            console.log("gagal wether")
        }
    });

}


function Temperature(response) {
    const { cloud, wind_mph, humidity, pressure_in } = response.current
    const { country, name } = response.location

    let temp = `
    <h4 class="card-title">Temp Guide</h4>
    <div class="d-flex align-items-center flex-row m-t-30">
        <div class="display-5 text-info"><i class="wi wi-day-showers"></i>
            <span>${cloud}<sup>°</sup></span></div>
        <div class="m-l-10">
            <h3 class="m-b-0">${getDay()}</h3><small>${name}, ${country}</small>
        </div>
    </div>
    <table class="table no-border mini-table m-t-20">
        <tbody>
            <tr>
                <td class="text-muted">Wind</td>
                <td class="font-medium">ESE ${wind_mph} mph</td>
            </tr>
            <tr>
                <td class="text-muted">Humidity</td>
                <td class="font-medium">${humidity}%</td>
            </tr>
            <tr>
                <td class="text-muted">Pressure</td>
                <td class="font-medium">${pressure_in} in</td>
            </tr>
            <tr>
                <td class="text-muted">Cloud Cover</td>
                <td class="font-medium">${cloud}%</td>
            </tr>
        </tbody>
    </table>
    <ul class="row list-style-none text-center m-t-30">
        <li class="col-3">
            <h4 class="text-info"><i class="wi wi-day-sunny"></i></h4>
            <span class="d-block text-muted">09:30</span>
            <h3 class="m-t-5">70<sup>°</sup></h3>
        </li>
        <li class="col-3">
            <h4 class="text-info"><i class="wi wi-day-cloudy"></i></h4>
            <span class="d-block text-muted">11:30</span>
            <h3 class="m-t-5">72<sup>°</sup></h3>
        </li>
        <li class="col-3">
            <h4 class="text-info"><i class="wi wi-day-hail"></i></h4>
            <span class="d-block text-muted">13:30</span>
            <h3 class="m-t-5">75<sup>°</sup></h3>
        </li>
        <li class="col-3">
            <h4 class="text-info"><i class="wi wi-day-sprinkle"></i></h4>
            <span class="d-block text-muted">15:30</span>
            <h3 class="m-t-5">76<sup>°</sup></h3>
        </li>
    </ul>
    `
    $("#temperatur").empty().append(temp)
}

// Get name
function getDay() {
    const today = new Date();

    // Daftar nama hari dalam Bahasa Inggris
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Mendapatkan indeks hari dalam seminggu (0 = Minggu, 1 = Senin, ..., 6 = Sabtu)
    const dayIndex = today.getDay();
    // Mendapatkan nama hari berdasarkan indeks
    const dayName = daysOfWeek[dayIndex];
    return dayName
}

// Get News
function getNews() {
    $.ajax({
        type: 'GET',
        url: "/get_news",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
            console.log(response.news.length)


                getCardNews(response.news)


            console.log("succes news")

        },
        error: function (error) {
            console.error(error);
        }
    });

}

function getCardNews(news){
    setTimeout(function() {
        $("#card-news").empty()
        console.log("Fungsi ini dijalankan setelah 2 detik");
        for (let index = 0; index < 2; index++) {
            let data = news[index];
            let nama = data.username.substring(0, 2).toUpperCase();
    
            let temp = 
            `
            <div class="d-flex flex-row comment-row">
            <div class="p-2 " >
                    <a
                    class="btn btn-circle d-flex btn-info text-white">${nama}</a>
                      
                    </div>
            <div class="comment-text active">
                <h6 class="font-medium">${data.username}</h6>
                <div class="pb-2">
                <img src="/static/${data.img}" alt="" style="width: 200px; height: 189px;" />
                </div>
                <span class="m-b-15 d-block ">${data.description}</span>
                <div class="comment-footer">
                    <span class="text-muted float-end">${moment(data.date).fromNow()}</span>
                    <span class="label label-success label-rounded">${data.topic}</span>
                    <span class="action-icons active">
                        <a href="/dashboard/admin/news"><i class="ti-pencil-alt"></i></a>
                       
                    </span>
                </div>
            </div>
        </div>
            `
        
        $("#card-news").append(temp)
        }
},5000)

   
   

}