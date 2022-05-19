/* On click toggle signin & Create Account Button */
$('.toggleBtn').click(function () {
    $('.toggleBtn').toggle();
  })
   
  /* On click SignIn button */
  $('.loginBtn').click(function () {
    $('#signUp').hide();
    $('#signIn').show();
    $('.passwordResetBtn').show();
    $('.passwordReset').hide(); 
  })
   
  /* On click password reset button */
  $('.passwordResetBtn').click(function () {
    $('#signUp').hide();
    $('#signIn').hide();
    $('.passwordReset').show(); 
    $('.loginBtn').show(); 
    $('.signUpBtn').hide();
  })
   
  /* On click create account button */
  $('.signUpBtn').click(function () {
    $('#signUp').show();
    $('#signIn').hide();
    $('.passwordReset').hide(); 
    $('.loginBtn').show(); 
    $('.passwordResetBtn').hide();
  })
   
  /* On click hide/show forms on mobile */
  $('.loginBtn-mobile').click(function () {
    $('#signUp').hide();
    $('#signIn').show();
    $('.passwordReset').hide(); 
  })
   
  $('.signUpBtn-mobile').click(function () {
    $('#signUp').show();
    $('#signIn').hide();
    $('.passwordReset').hide(); 
  })
   
  /* On click reset button */
  $('.forgotPassword').click(function () {
    $('#signUp').hide();
    $('#signIn').hide();
    $('.passwordReset').show(); 
  })