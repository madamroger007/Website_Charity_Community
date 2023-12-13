document.addEventListener('DOMContentLoaded', function () {

    /* initialize the calendar
    -----------------------------------------------------------------*/

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
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
            console.log("berhasil")
            console.log(response.timestamp_users)
            console.log("berhasil")



        },
        error: function (error) {
            console.error(error);
        }
    });

}

function InfoCard(total) {
    // Mengubah format tanggal dari "YYYY-MM-DD-HH-mm-ss" menjadi "DD MMMM YYYY, HH:mm:ss"
    // let time_update_user = 
    let temp = `
    <li class="feed-item">
    <div class="feed-icon bg-info"><i class="mdi mdi-account-multiple-plus"></i></div> Total ${total.total_users} User  <span class="ms-auto font-12 text-muted">${moment(total.timestamp_users).fromNow()}</span>
</li>
<li class="feed-item">
    <div class="feed-icon bg-success"><i class="mdi mdi-currency-usd"></i></div> Total $${total.total_donation} Donate <span class="ms-auto font-12 text-muted">${moment(total.timestamp_donations).fromNow()}</span>
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
}

// Get donate
function getDonate() {
    $.ajax({
        type: 'GET',
        url: "/get_donate",
        success: function (response) {
            // Perbarui tabel dengan data pengguna baru
     
            updateTableContent(response.donation)
           

        },
        error: function (error) {
            console.error(error);
        }
    });

}

function updateTableContent(donation) {
    // Tambahkan data pengguna baru ke tabel
    for (let index = 0; index < donation.length; index++) {
        let donate = donation[index];
        let nama = donate.username.substring(0, 2).toUpperCase();
        let row = `
        <tr class="pt-2">
        <td class="d-flex align-items-center justify-content-center"><p>1</p></td>
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
        <h5 class="m-b-0">${toRupiah(donate.donation_amount,{symbol: 'IDR', floatingPoint: 0}) }</h5>
        </td>
        <td>${moment(donate.date).fromNow()}</td>
    </tr>
           
`;
        $('#donation-form').append(row);
    }
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

function getDay(){
    const today = new Date();

    // Daftar nama hari dalam Bahasa Inggris
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Mendapatkan indeks hari dalam seminggu (0 = Minggu, 1 = Senin, ..., 6 = Sabtu)
    const dayIndex = today.getDay();
    // Mendapatkan nama hari berdasarkan indeks
    const dayName = daysOfWeek[dayIndex];
    return dayName
}

function Temperature(response){
   const {cloud,wind_mph,humidity,pressure_in} = response.current
   const {country,name} = response.location

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