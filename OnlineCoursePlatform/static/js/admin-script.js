$(document).ready(function () {

    initialize_tables();

    //selectable rows feature
    var activeRow = null;
    $('.datatable').on('click', 'tbody tr', function () {
        $('.btn.edit').attr("disabled", true);
        $('.btn.remove').attr("disabled", true);
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
                activeRow = null;
            }
            else {
            var lists = ['personlist', 'unilist', 'studentlist', 'lecturerlist', 'courselist', 'commentlist', 'reportlist']
                for(var i=0; i<lists.length; i++){
                    var tableid = '#'+lists[i];
                    $(tableid).DataTable().$('tr.selected').removeClass('selected');
                }

                $(this).addClass('selected');
                $('.btn.edit').attr("disabled", false);
                $('.btn.remove').attr("disabled", false);
                activeRow = this;
            }
        });

        //edit row action
        $('.edit').on('click',function(){
        var table_id = $(activeRow).closest('table').attr('id');
        auto_fill_modal(activeRow, table_id, 'edit');
        $(".modal").css("display", "block");
        });

        //add row action
        $('.add').on('click',function(){
            table_id = this.closest('div').getElementsByTagName('table')[0].id
            auto_fill_modal(activeRow, table_id, 'add');
           $(".modal").css("display", "block");
        });

        $('.change').on('click', function(){
            var id = $('#inputid').val();
            var tableid = $('#header').text();
            var newvalue1 = $('#input1').val();
            var newvalue2 = $('#input2').val();
            var newvalue3 = $('#input3').val();
            var newvalue4 = $('#input4').val();
            var newvalue5 = $('#input5').val();
            var newvalue6 = $('#input6').val();
            var newvalue7 = $('#input7').val();
            var newvalue8 = $('#input8').val();
            post_data(id, newvalue1, newvalue2, newvalue3, newvalue4, newvalue5, newvalue6, newvalue7, newvalue8, tableid, intent);

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
                "name": "ID",
                
            },
            {
                "name": "First Name",
                
            },
            {
                "name": "Last Name",
                
            },
            {
                "name": "Email",
                
            },
            {
                "name": "Password",
                
            },
            {
                "name": "Birthdate",
                
            },
            {
                "name": "Address",
                
            },
            {
                "name": "Phone",
                
            },
            {
                "name": "Person Type",
                
            },
        ]
    });
    
    var unilist = $('#unilist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('university') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",
                
            },
            {
                "name": "Name",
                
            },
            {
                "name": "Location",
                
            },
        ]
    });

    var studentlist = $('#studentlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('student') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "Univeristy ID",

            },
        ]
    });
    var lecturerlist = $('#lecturerlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('lecturer') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "University ID",

            },
        ]
    });
    var courselist = $('#courselist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('course') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "Title",

            },
            {
                "name": "Description",

            },
            {
                "name": "Price",

            },
            {
                "name": "Video Link",

            },
            {
                "name": "Category",

            },
            {
                "name": "Lecturer ID",

            },
            {
                "name": "Thumbnail",

            },
        ]
    });
    var commentlist = $('#commentlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('comment') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "Person ID",

            },
            {
                "name": "Description",

            },
            {
                "name": "Title",

            },
            {
                "name": "Course ID",

            },
            {
                "name": "Post Date",

            },
        ]
    });
    var reportlist = $('#reportlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('report') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "Student ID",

            },
            {
                "name": "Description",

            },
            {
                "name": "Course ID",

            },
            {
                "name": "Report Date",

            },
        ]
    });
    var reportlist = $('#reportlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('report') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "Student ID",

            },
            {
                "name": "Description",

            },
            {
                "name": "Course ID",

            },
            {
                "name": "Report Date",

            },
        ]
    });
    var orderlist = $('#orderlist').DataTable({
        "ajax": {
            "processing": true,
            "url": "/reloadtable/",
            "data": { 'table_id': JSON.stringify('report') },
            "dataType": "json",
            "dataSrc": ""
        },

        "iDisplayLength": 25,
        "columns": [
            {
                "name": "ID",

            },
            {
                "name": "Student ID",

            },
            {
                "name": "Course ID",

            },
            {
                "name": "Ordered Date",

            },
        ]
    });

}

function auto_fill_modal(activeRow, table_id,  action) {
    //automatically hides unneccessary elements and renames the rest according to the table
    $('.modal-input').css('display','block');
    $('.modal-label').css('display','block');
    $('.modal-input').val("");

    var jquery_tableid = '#'+table_id;
    var table = $(jquery_tableid).DataTable();
    table_row = table.row(activeRow).data();
    $('#inputid').val(table_row[0]);
    $('#inputintent').val(action);

    switch (table_id) {
        case 'personlist':
            $('#header').val('person');
            var person = ['ID','First Name','Last Name', 'Email','Password','Birthdate','Address','Phone','Person Type']
            for(var i=1; i<9; i++){
            var labelid='#label'+i;
            $(labelid).text(person[i-1]);
            if(action=='edit'){
            var inputid='#input'+i;
            $(inputid).val(table_row[i-1]);
            }

            }
            break;
        case 'unilist':
            $('#header').val('university');
            var uni = ['ID','Name','Location']
            for(var i=1; i<4; i++){
                var labelid='#label'+i;
                $(labelid).text(uni[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i-1]);
                }
            }
        break;
        case 'studentlist':
        $('#header').val('student');
        var stu = ['ID','University ID']
            for(var i=1; i<3; i++){
            var labelid='#label'+i;
                $(labelid).text(stu[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i-1]);
                }
            }
            break;
        case 'lecturerlist':
            $('#header').val('lecturer');
            var lect = ['ID','University ID']
            for(var i=1; i<3; i++){
            var labelid='#label'+i;
                $(labelid).text(lect[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i-1]);
                }
            }
        break;
        case 'courselist':
        $('#header').val('course');
        var course = ['ID','Title', 'Description', 'Price', 'Video Link', 'Category', 'Lecturer ID', 'Thumbnail']
            for(var i=1; i<8; i++){
            var labelid='#label'+i;
                $(labelid).text(course[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i-1]);
                }
            }
            break;
        case 'commentlist':
        $('#header').val('comment');
        var comment = ['ID',  'Person ID', 'Description', 'Title', 'Course ID', 'Post Date']
            for(var i=1; i<7; i++){

            var labelid='#label'+i;
                $(labelid).text(comment[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i]);
                }
            }
            break;

        case 'reportlist':
        $('#header').val('report');
        var report = ['ID',  'Student ID', 'Description', 'Course ID', 'Report Date']
            for(var i=1; i<6; i++){
            var labelid='#label'+i;
                $(labelid).text(report[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i-1]);
                }
            }
            break;
        case 'orderlist':
        $('#header').val('order');
        var order = ['ID',  'Student ID', 'Course ID', 'Order Date']
            for(var i=1; i<5; i++){
            var labelid='#label'+i;
                $(labelid).text(order[i-1]);
                if(action=='edit'){
                var inputid='#input'+i;
                $(inputid).val(table_row[i-1]);
                }
            }
            break;
    }
    //after auto filling inputs, hide extra input and label elements
    for(i ; i<9; i++){
                var labelid='#label'+i;
                var inputid='#input'+i;
                $(labelid).css('display','none');
                $(inputid).css('display','none');
    }
}


 function closeModal(modalid){
     var jquery_tableid = '#'+modalid;
     $(jquery_tableid).css('display','none');
 }

 function post_data(id, newvalue1, newvalue2, newvalue3, newvalue4, newvalue5, newvalue6, newvalue7, newvalue8, tableid, intent) {
    // id == -999 represents DB will assign auto-incremental id
    $.ajax({
        type: "POST",
        url: '/processdata/',
        data: {
            'intent': JSON.stringify(intent),
            'table_id': JSON.stringify(tableid.replace('list', '')),
            'data_id': JSON.stringify(id),
            'newvalue1': JSON.stringify(newvalue1),
            'newvalue2': JSON.stringify(newvalue2),
            'newvalue3': JSON.stringify(newvalue3),
            'newvalue4': JSON.stringify(newvalue4),
            'newvalue5': JSON.stringify(newvalue5),
            'newvalue6': JSON.stringify(newvalue6),
            'newvalue7': JSON.stringify(newvalue7),
            'newvalue8': JSON.stringify(newvalue8),
        },
        dataType: "json",
    }).done(function (response) {
        if (response['status'] == '200') {
            refresh(tableid);
            closeModal('editModal');
        }
        else
            alert(response['response']);
        enable_btn();
    });
}

function refresh(table_id) {
    var element = '#' + table_id
    var table = $(element).DataTable();
    table.ajax.reload();
}