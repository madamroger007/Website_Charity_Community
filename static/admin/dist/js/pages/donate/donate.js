$(document).ready(function () {
    updateTable()

});

function updateTable() {
    // Ambil data pengguna baru dan perbarui tabel
    $.ajax({
        type: 'GET',
        url: "/get_donate",
        success: function (response) {
            console.log(response)
            // Perbarui tabel dengan data pengguna baru
            updateTableContent(response.donation);
            console.log(response.total_donation)
        },
        error: function (error) {
            console.error(error);
        }
    });
}

function updateTableContent(donation) {
    // Hapus semua baris tabel kecuali header
    setTimeout(function() {
        console.log("Fungsi ini dijalankan setelah 2 detik");
        $('#donate-form').empty();

    // Tambahkan data pengguna baru ke tabel
    for (let index = 0; index < donation.length; index++) {
        let user = donation[index];
        let row = `
<tr>
    <th scope="row">${(index + 1)}</th>
    <td>${user.username}</td>
    <td>${user.country}</td>
    <td>${toRupiah(user.donation_amount, { symbol: 'IDR', floatingPoint: 0 })}</td>
    <td>${user.email}</td>
    <td>${user.agree}</td>
    <td>${user.phone}</td>
    <td>${user.bank_account}</td>
    <td>${user.date}</td>
    
</tr>`;
        $('#donate-form').append(row);
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

        },
        error: function (error) {
            // Handle error, e.g., show an alert
            console.error(error);
        }
    })
}