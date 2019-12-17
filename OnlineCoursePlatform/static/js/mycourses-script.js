$(document).ready(function () {

var studentid = $('#personid').val();
console.log('personid'+studentid);
get_courses(studentid);
});

function get_courses(studentid){
//when user navigates to mycourses page, load user's courses to the listview. If no any couses, then warn
     $.ajax({
             type: "POST",
             url: '/get-data/',
             data: {
             'studentid': JSON.stringify(studentid),
             },
             dataType: "json",
          }).done(function (response) {
                        if (response['response'] == '200'){
                        var ordered_courses = response['data']
                        console.log(ordered_courses);
                        }
                        else
                            $('#noCourse').addClass('visible').removeClass('hidden');
           });
}