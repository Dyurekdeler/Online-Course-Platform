$(document).ready(function () {

var studentid = $('#personid').val();
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
                for(i=0; i<ordered_courses.length; i++){
                    console.log(ordered_courses[i][0]); //id




                    var str = ''
                    ordered_courses.forEach(function(course) {
                        str += '<a href="#" class="list-group-item">'+ '<img class="thumbnail" src="">' +course[0] + '</a>';
                    });


                    document.getElementById("myCoursesList").innerHTML = str;
                }

             }
              else
                $('#noCourse').addClass('visible').removeClass('hidden');
     });
}