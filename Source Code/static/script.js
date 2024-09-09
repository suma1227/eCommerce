
function onClickLogin(item) {
    var admin_page = document.getElementById("admin_page");
    var customer_page = document.getElementById("customer_page");

    if (item === 'admin_page') {
        admin_page.style.display = "";
        customer_page.style.display = "none";
    } else if (item === 'customer_page') {
        admin_page.style.display = "none";
        customer_page.style.display = "";
    }
}


function newCustomerLogin(item) {
    var newCustomer = document.getElementById("newCustomer");
    var customer_page = document.getElementById("customer_page");

    if (item === 'newCustomer') {
        newCustomer.style.display = "block";
        customer_page.style.display = "none";
    } else {
        newCustomer.style.display = "none";
        customer_page.style.display = "block";
    }
}


   function validate(){
        var regex_care_name = /^[a-zA-Z ]*$/;
        var card_name = document.getElementById("card_name").value
        if(!regex_care_name.test(card_name)){
            alert("Invalid Name on Card")
            return false
        }

        var card_number = document.getElementById("card_number").value
        if(card_number.length!=16){
            alert("Card Number Should be 16")
            return false
        }

        var expiry_date = document.getElementById("expiry_date").value
        if(expiry_date.length!=5){
            alert("Invalid Expire Date")
            return false
        }

        var cvv = document.getElementById("cvv").value
        if(cvv.length!=3){
            alert("Invalid CVV")
            return false
        }

        return true
    }

