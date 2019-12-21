$(document).ready(function () {

    initialize_tables();

    //selectable rows
    var activeRow = null;
    $('.datatable').on('click', 'tbody tr', function () {
        $('.btn.edit').attr("disabled", true);
        $('.btn.remove').attr("disabled", true);
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
                activeRow = null;
            }
            else {
                $('#personlist').DataTable().$('tr.selected').removeClass('selected');

                $(this).addClass('selected');
                $('.btn.edit').attr("disabled", false);
                $('.btn.remove').attr("disabled", false);
                activeRow = this;
            }
        });

        $('.edit').on('click',function(){
        auto_fill_modal(activeRow,'personlist');
           $(".modal").css("display", "block");

        });

        $('.add').on('click',function(){
            reset_elements();
            set_elements('personlist');
           $(".modal").css("display", "block");
        });

});

function initialize_tables() {
    var personlist = $('#personlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('person') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "Person ID",
                "class": "personlist-cell",
            },
            {
                "name": "First Name",
                "class": "personlist-cell",
            },
            {
                "name": "Last Name",
                "class": "personlist-cell",
            },
            {
                "name": "Email",
                "class": "personlist-cell",
            },
            {
                "name": "Password",
                "class": "personlist-cell",
            },
            {
                "name": "Birthdate",
                "class": "personlist-cell",
            },
            {
                "name": "Address",
                "class": "personlist-cell",
            },
            {
                "name": "Phone",
                "class": "personlist-cell",
            },
            {
                "name": "Person Type",
                "class": "personlist-cell",
            },
        ]
    });
}

function auto_fill_modal(activeRow, table_id) {
    //automatically hides and fills inputs&labels of editmodal
    reset_elements();
    var table = $('#personlist').DataTable();
    table_row = table.row(activeRow).data();

    set_elements(table_id);
    switch (table_id) {
        case 'personlist':
            document.getElementById('input1').value = table_row[1];
            document.getElementById('input2').value = table_row[2];
            document.getElementById('input3').value = table_row[3];
            break;
    }
}
function auto_fill(table_id){
//automatically hides and fills inputs&labels of editmodal
    reset_elements();
    set_elements(table_id);
    document.getElementById('input1').value = "";
    document.getElementById('input2').value = "";
    document.getElementById('input3').value = "";
    switch (table_id) {
        case 'personlist':
            document.getElementById('input3').style.display = "none";
            break;
    }
}

function reset_elements(){
    document.getElementById('input1').style.display = "block";
    document.getElementById('input2').style.display = "block";
    document.getElementById('input3').style.display = "block";
    document.getElementById('label1').style.display = "block";
    document.getElementById('label2').style.display = "block";
    document.getElementById('label3').style.display = "block";
    document.getElementById('input1').defaultValue = "";
    document.getElementById('input2').defaultValue = "";
    document.getElementById('input3').defaultValue = "";
}

 function set_elements(table_id){
 switch (table_id) {
        case 'personlist':
            document.getElementById('label1').innerHTML = 'Name';
            document.getElementById('label2').innerHTML = 'ISO31661a2Code';
            document.getElementById('label3').innerHTML = 'ISO31661a3Code';
            document.getElementById("header").innerHTML = 'Person List'
            break;
 }
 }