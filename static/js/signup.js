function redirectToSignup() {
    var customerRadio = document.getElementById("customer");
    var storeManagerRadio = document.getElementById("store-manager");
    var appManagerRadio = document.getElementById("app-manager");
  
    if (customerRadio.checked) {
      window.location.href = "/customer_signup";
    } else if (storeManagerRadio.checked) {
      window.location.href = "/store_manager_signup";
    } else if (appManagerRadio.checked) {
      window.location.href = "/app_manager_signup";
    } else {
      alert("Please select a role before proceeding to sign up.");
    }
}