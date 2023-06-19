function redirectToSignup() {
    var customerRadio = document.getElementById("customer");
    var storeManagerRadio = document.getElementById("store-manager");
    var deliveryExecutiveRadio = document.getElementById("delivery-executive");
    
    if (customerRadio.checked) {
      window.location.href = "/customer_signup";
    } 
    else if (storeManagerRadio.checked) {
      window.location.href = "/store_manager_signup";
    } 
    else if (deliveryExecutiveRadio.checked) {
      window.location.href = "/delivery_executive_signup";
    } 
    
    else {
      alert("Please select a role before proceeding to sign up.");
    }
}