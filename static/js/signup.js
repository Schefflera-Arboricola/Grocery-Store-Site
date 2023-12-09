function redirectToSignup() {
    var customerRadio = document.getElementById("customer");
    var adminRadio = document.getElementById("admin");
    var storeManagerRadio = document.getElementById("store-manager");
    var deliveryExecutiveRadio = document.getElementById("delivery-executive");
    var developerRadio = document.getElementById("developer");
    
    if (customerRadio.checked) {
      window.location.href = "/customer_signup";
    } 
    else if (adminRadio.checked) {
      alert("Admin signup is not allowed. Please contact the developer to get access to the admin's username and password.")
    }
    else if (storeManagerRadio.checked) {
      window.location.href = "/store_manager_signup";
    } 
    else if (deliveryExecutiveRadio.checked) {
      window.location.href = "/delivery_executive_signup";
    } 
    else if (developerRadio.checked) {
      window.location.href = "/developer_signup";
    }
    else {
      alert("Please select a role before proceeding to sign up.");
    }
}

function redirectToForgotPswd(){
    var customerRadio = document.getElementById("customer");
    var adminRadio = document.getElementById("admin");
    var storeManagerRadio = document.getElementById("store-manager");
    var deliveryExecutiveRadio = document.getElementById("delivery-executive");
    var developerRadio = document.getElementById("developer");
    
    if (customerRadio.checked) {
      window.location.href = "/customer_forgot_password";
    } 
    else if (adminRadio.checked) {
      alert("Admin forgot password is not allowed. Please contact the developer to get the admin password.")  
    }
    else if (storeManagerRadio.checked) {
      window.location.href = "/store_manager_forgot_password";
    } 
    else if (deliveryExecutiveRadio.checked) {
      window.location.href = "/delivery_executive_forgot_password";
    } 
    else if (developerRadio.checked) {
      window.location.href = "/developer_forgot_password";
    }
      else {
      alert("Please select a role.");
    }
}