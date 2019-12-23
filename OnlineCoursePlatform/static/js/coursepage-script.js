$(document).ready(function(){

    $('.buyCourse').on('click', function(){
        var course_id = this.id;
        $.ajax({
                        type: "POST",
                        url: '/buy-course/',
                        data: {
                            'course_id': JSON.stringify(course_id),
                        },
                        dataType: "json",
                    }).done(function (response) {

                    });

    });

    $('#report').on('click', function(){
        $("#reportModal").css("display", "block");
    });
    $('.close').on('click', function(){
        $("#reportModal").css("display", "none");
    });

});