var fnameError = document.getElementById('fname-error')
var lnameError = document.getElementById('lname-error')
var phoneError = document.getElementById('phone-error')
var emailError = document.getElementById('email-error')
var password1Error = document.getElementById('password1-error')
var password2Error = document.getElementById('password2-error')
var submitError = document.getElementById('btn-Error')

function validateFName(){
    var name = document.getElementById('firstname_id').value;

    if(name.length == 0){
        fnameError.innerHTML = 'Name required';
        return false;
    }
    if(!name.match(/^[a-zA-Z ]+$/)){
        fnameError.innerHTML = 'Name cannot contain numbers';
        return false;
    }
    fnameError.innerHTML = '<i class="fa fa-check" aria-hidden="true" style="color:green;"></i>';
    console.log("firstname true")

    return true;
}
function validateLName(){
    var name = document.getElementById('lastname_id').value;

    if(name.length == 0){
        lnameError.innerHTML = 'Name required';
        return false;
    }
    if(!name.match(/^[a-zA-Z ]+$/)){
        lnameError.innerHTML = 'Name cannot contain numbers';
        return false;
    }
    lnameError.innerHTML = '<i class="fa fa-check" aria-hidden="true" style="color:green;"></i>';
    console.log("Lname true")
    return true;
}


function validatePhone(){
    var mobile = document.getElementById('phone_id').value;
    console.log(mobile)
    if(mobile.length==0){
        phoneError.innerHTML = 'Mobile no required'
        return false;
    }
    if(mobile.length !==10){
        phoneError.innerHTML = 'Mobile no should be 10 digits'
        return false;
    }
    if(!mobile.match(/^[0-9]{10}$/)){
        phoneError.innerHTML = 'Mobile no required';
        return false;
    }
    phoneError.innerHTML = '<i class="fa fa-check" aria-hidden="true" style="color:green;"></i>';
    console.log("Phone true")
    return true;
}
function validateEmail(){
    var email =  document.getElementById('email_id').value;
    if(email.length==0){
        emailError.innerHTML = 'Email required'
        return false;
    }
    if(!email.match(/^[A-Za-z\._\-[0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/)){
        emailError.innerHTML = 'Email Invalid'
        return false;
    }
    emailError.innerHTML = '<i class="fa fa-check" aria-hidden="true" style="color:green;"></i>';
    console.log("Email true")
    return true;
}
function validatePass1(){
    var pass= document.getElementById('password1_id').value;
    // document.getElementById('password2_id').value=''
    console.log(pass)
    if(pass.length==0){
        password1Error.innerHTML="Please include password"
        return false;
    }
    if(!pass.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,15}$/)){
        password1Error.innerHTML ='Password must contain Minimum eight characters, at least one letter and one number  '
        return false;

    }
    password1Error.innerHTML ='<i class="fa fa-check" aria-hidden="true" style="color:green;"></i>';
    console.log("pass1 true")
    return true;
}
function validatePass2(){
    var pass2= document.getElementById('password2_id').value;
    var pass1= document.getElementById('password1_id').value;
    console.log(pass2)
    if(pass2.length==0){
        password2Error.innerHTML="Please Conform password"
        return false;
    }
    // if(!pass.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,15}$/)){
    //     password2Error.innerHTML ='Password must contain Minimum eight characters, at least one letter and one number  '
    //     return false;

    // }
    if(pass1!=pass2){
        password2Error.innerHTML ="Password not matching "
        return false;
    }
    password2Error.innerHTML ='<i class="fa fa-check" aria-hidden="true" style="color:green;"></i>';
    return true;
}

function validatePass2focus(){
    password2Error.innerHTML=" ";
    return true
}





function validateForm(){
    if(!validateFName() || !validateLName() || !validatePhone() || !validateEmail() || !validatePass1() || !validatePass2() ){
        submitError.style.display = 'block';
        submitError.innerHTML = 'Please fix error to submit'
        setTimeout(function(){submitError.style.display = 'none';}, 3000);
        return false;
    }
}