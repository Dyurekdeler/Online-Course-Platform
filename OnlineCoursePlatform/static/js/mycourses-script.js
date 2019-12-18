$(document).ready(function () {

var ajaxResponse = [];
var studentid = $('#personid').val();
ajaxResponse = get_courses(studentid);

$('#myCoursesList').on('click','.list-group-item', function(){
    var courseid = this.id;
$.ajax({
         type: "POST",
         url: '/course/',
         data: {
         'course_detail': JSON.stringify(ajaxResponse),
         },
         dataType: "json",
         }).done(function (response) {

         });


});


function get_courses(studentid){
var response = [];
//when user navigates to mycourses page, load user's courses to the listview. If no any couses, then warn
     $.ajax({
         type: "POST",
         url: '/get-data/',
         async:true,
         data: {
         'studentid': JSON.stringify(studentid),
         },
         dataType: "json",
         }).done(function (response) {
             if (response['response'] == '200'){
                var ordered_courses = response['data'];
                response.push(response['data']);
                for(i=0; i<ordered_courses.length; i++){
                    //id , title , desc, price, link, category, lec, thumbnail

                    var str = ''
                    ordered_courses.forEach(function(course) {
                        str += '<button id="'+course[0]+'" class="list-group-item">hello</button><img class="thumbnail" src="'+course[7]+'">' + course[1] +'<p>'+course[2]+'</p>';
                    });

                    document.getElementById("myCoursesList").innerHTML = str;
                }

             }
              else
                $('#noCourse').addClass('visible').removeClass('hidden');
     });
     return response;
}
