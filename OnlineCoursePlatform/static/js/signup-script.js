$(document).ready(function () {

    //as user selects an option from uni combobox, write it to a hidden input element for form action
    var uni = document.getElementById("university");
    uni.value= 1;
    $('#uni-selection').on('click', function() {
        var selection = document.getElementById("uni-selection");
        var selVal = selection.options[selection.selectedIndex].value;
        uni.value= selVal;
        console.log(uni.value);
    });
    var person_type = document.getElementById("person_type");
    person_type.value= 'STU';
    $('#persontype-selection').on('click', function() {
        var selection = document.getElementById("persontype-selection");
        var selVal = selection.options[selection.selectedIndex].value;
        person_type.value= selVal;
        console.log(person_type.value);
    });
});