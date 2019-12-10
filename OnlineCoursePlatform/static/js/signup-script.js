$(document).ready(function () {

    //hiddenly fill user's uni selection into an input for form control
    var uni = document.getElementById("university");
    uni.value= 1;
    $('#uni-selection').on('click', function() {
        var selection = document.getElementById("uni-selection");
        var selVal = selection.options[selection.selectedIndex].value;
        uni.value= selVal;
    });
});