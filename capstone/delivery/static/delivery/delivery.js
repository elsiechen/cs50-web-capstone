document.addEventListener('DOMContentLoaded', function(){
  // Update the cart_button with order item qty
  if (localStorage.getItem('item_qty')){
    var cartitemsqty = JSON.parse(localStorage.getItem('item_qty')); 
    document.querySelector('#cart_button').innerHTML = `🛒&nbsp;Cart-${cartitemsqty}`;
  }

  // Order.html
  openButtons = document.querySelectorAll('.open_button');
  closeButtons = document.querySelectorAll('.close_button');

  // Press menuItem to show the listingItem
  openButtons.forEach(function(openButton) {
    openButton.addEventListener('click', function(){
      item_id=this.dataset.openid;
      document.querySelector('body').style.backgroundColor = 'grey';
      listingItem_container = document.querySelector(`div[data-listingid="${item_id}"]`);
      listingItem_container.style.display = 'block';
      // Get all the children of the div and disable them within a loop
      var childNodes = document.querySelector('.menu').getElementsByTagName('*');
      for (var node of childNodes) {
        node.disabled = true;
      }
      // Set opacity of menu view to 0.5
      document.querySelector('.menu').style.opacity = '0.5';
      
          
    });
  });
  // Press closeButton to close the listingItem
  closeButtons.forEach(function(closeButton) {
    closeButton.addEventListener('click', function(){
      item_id = this.dataset.closebuttonid;
      document.querySelector('body').style.backgroundColor = 'white';
      listingItem_container = document.querySelector(`div[data-listingid="${item_id}"]`);
      listingItem_container.style.display = 'none';
      // Get all the children of the div and activate them within a loop
      var childNodes = document.querySelector('.menu').getElementsByTagName('*');
      for (var node of childNodes) {
        node.disabled = false;
      }
      // Undo the setting of opacity of menu view
      document.querySelector('.menu').style.opacity = '1';
    });
  });
  

  add_buttons = document.querySelectorAll('.add_button');
  minus_buttons = document.querySelectorAll('.minus_button');
  plus_buttons = document.querySelectorAll('.plus_button');
  qtys = document.querySelectorAll('.qty');
  

  minus_buttons.forEach(function(minus_button){
    minus_button.addEventListener('click', function(){
      item_id = this.dataset.minusid;
      // Qty minus one if qty > 1
      qty = parseInt(document.querySelector(`#qty_${item_id}`).innerHTML);
      if (qty > 1){
        updated_qty = qty - 1;
        document.querySelector(`#qty_${item_id}`).innerHTML = updated_qty;
      } 
      
    // Update add_button qty and total_price
      // Get radio button value of size       
      radio = document.getElementsByName(item_id);     
      for(var i=0; i<radio.length; i++){
        if(radio[i].checked){
          size = radio[i].value;
        }
      }
      price = parseFloat(document.querySelector(`#price_${item_id}`).value);
  
      // Small(size value=3) price equal to price-3
      if (size == "3") 
        order_price = price - 3.00;           
      // Medium(size value=1) price equal to price
      if (size == "1")
        order_price = price;     
      // Large(size value=2) price equal to price+4
      if (size == "2") 
        order_price = price + 4.00;
      console.log(size);
      total_price = order_price*updated_qty;
      
      console.log(price);
      console.log(order_price);
      console.log(updated_qty);
      console.log(total_price);
      // Update the value of add_button with qty and total price
      document.querySelector(`#addbutton_${item_id}`).innerHTML = "Add&nbsp;&nbsp;"+ updated_qty +"&nbsp;&nbsp;to Order&nbsp;&nbsp$" + total_price.toFixed(2);  

    });
  });

  plus_buttons.forEach(function(plus_button){
    plus_button.addEventListener('click', function(){
      item_id = this.dataset.plusid;
      qty = parseInt(document.querySelector(`#qty_${item_id}`).innerHTML);
      updated_qty = qty + 1;
      document.querySelector(`#qty_${item_id}`).innerHTML = updated_qty;  
      
      // Update add_button qty and total_price
      // Get radio button value of size       
      radio = document.getElementsByName(item_id);     
      for(var i=0; i<radio.length; i++){
        if(radio[i].checked){
          size = radio[i].value;
        }
      }
      price = parseFloat(document.querySelector(`#price_${item_id}`).value);
  
      // Small(size value=3) price equal to price-3
      if (size == "3") 
        order_price = price - 3.00;           
      // Medium(size value=1) price equal to price
      if (size == "1")
        order_price = price;     
      // Large(size value=2) price equal to price+4
      if (size == "2") 
        order_price = price + 4.00;
      console.log(size);
      total_price = order_price*updated_qty;
      
      console.log(price);
      console.log(order_price);
      console.log(updated_qty);
      console.log(total_price);
      // Update the value of add_button with qty and total price
      document.querySelector(`#addbutton_${item_id}`).innerHTML = "Add&nbsp;&nbsp;"+ updated_qty +"&nbsp;&nbsp;to Order&nbsp;&nbsp$" + total_price.toFixed(2);  

    });
  });


  add_buttons.forEach(function(add_button) {
    add_button.addEventListener('click', function() {
      item_id = this.dataset.addbuttonid;
      qty = parseInt(document.querySelector(`#qty_${item_id}`).innerHTML);
      
      // Get radio button value of size 
      radio = document.getElementsByName(item_id)
      for(i=0; i<radio.length; i++){
        if(radio[i].checked){
          size = radio[i].value;
        }
      }
      
      // Get the order_price based on size
      price = parseFloat(document.querySelector(`#price_${item_id}`).value);
        // Small(size value=3) price equal to price-3
      if (size == "3"){ 
        order_price = price - 3.00;        
      }
        // Medium(size value=1) price equal to price
      if (size == "1"){ 
        order_price = price;
      }
        // Large(size value=2) price equal to price+4
      if (size == "2"){ 
        order_price = price + 4.00;
      }

      // Update the cart_button qty with item qty
      cart_button = document.querySelector('#cart_button');
        // Store cart_item_qty, if no item_qty in local storage
      if (!localStorage.getItem('item_qty')){        
        localStorage.setItem('item_qty', JSON.stringify(qty));
        cart_button.innerHTML = "🛒&nbsp;Cart-" + qty;
      } else {
        //Retrieve the current cart_item_qty and convert them back to an string
        var cartitems_qty = JSON.parse(localStorage.getItem('item_qty'));
        updated_qty = parseInt(cartitems_qty)+qty;
        localStorage.setItem('item_qty', JSON.stringify(updated_qty));
        cart_button.innerHTML = "🛒&nbsp;Cart-" + updated_qty;        
      }

      console.log(item_id);
      console.log(qty);
      console.log(JSON.parse(localStorage.getItem('item_qty')));

      document.querySelector('body').style.backgroundColor = 'white';
      listingItem_container = document.querySelector(`div[data-listingid="${item_id}"]`);
      listingItem_container.style.display = 'none';
      // Get all the children of the div and activate them within a loop
      var childNodes = document.querySelector('.menu').getElementsByTagName('*');
      for (var node of childNodes) {
        node.disabled = false;
      }
      // Undo the setting of opacity of menu view
      document.querySelector('.menu').style.opacity = '1';


      fetch(`/orderitem/${item_id}`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
                              item_qty: qty,
                              item_size: size, 
                              item_price: order_price
                            }),
      })
      .then(response => response.json())
      .then(result => {
        console.log(result)
      });
    });
  });


  // Cart.html
  document.querySelector('#time-view').style.display = 'none';
   // press the time_button to display the selection list of date and time
  document.querySelector('#time_button').addEventListener('click', function(){
    document.querySelector('#time-view').style.display = 'block';      
  });

  // press the time_form_button(Schedule) to close the selection list and replace the content of delivery time
  document.querySelector('#time_form_button').addEventListener('click', function(){
      date = document.querySelector('#date').selectedOptions[0].value;
      time = document.querySelector('#time').selectedOptions[0].value;
      document.querySelector('#time_button').value = "Delivery Time:&nbsp;"+ date + "&nbsp;&nbsp;" + time;  
      document.querySelector('#time-view').style.display = 'none';
      console.log(date);
      console.log(time);
  });

  // press the delivery_now_button to close the selection list and replace the content of delivery time
  document.querySelector('#delivery_now_button').addEventListener('click', function(){
    d = new Date();
    document.querySelector('#time_button').value = "Delivery Now";
    document.querySelector('#time-view').style.display = 'none';  
  });
  
  // Change order item qty in cart and update it using fetch
  select_qtys = document.querySelectorAll('.select_qty');
  select_qtys.forEach(function(select_qty){
    select_qty.addEventListener('change', function(){
      item_id = this.dataset.selectqtyid;
      console.log(item_id)
      update_qty = document.querySelector(`#select_qty_${item_id}`).selectedOptions[0].value;
      fetch(`/updateitem/${item_id}`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
                              item_qty: update_qty,
                            }),
      })
      .then(response => response.json())
      .then(result => {
        console.log(result.status);
        console.log(result.total_qty)
        // Delete order item list in cart if item_qty = 0 (remove)
        if (result.updateqty == 0){
          document.querySelector(`#select_item_${item_id}`).style.display = 'none';
        }
        //Update the current cart_item_qty 
        localStorage.setItem('item_qty', JSON.stringify(result.total_qty));
        cart_button.innerHTML = "🛒&nbsp;Cart-" + result.total_qty; 
        // Update the fields: subtotal, delivery, tax, total
        document.querySelector('#subtotal').innerHTML= "$&nbsp;" + result.subtotal;
        document.querySelector('#d_fee').innerHTML= "$&nbsp;" + result.d_fee;
        document.querySelector('#tax').innerHTML= "$&nbsp;" + result.tax;
        document.querySelector('#total').innerHTML= "$&nbsp;" + result.total;
        console.log(result.tax);
      })
    });
  });

  // press place order btn 
  document.querySelector('#place_order').addEventListener('click', function(){
    //Update the current cart_item_qty to 0
    localStorage.setItem('item_qty', JSON.stringify(0));
    cart_button.innerHTML = "🛒&nbsp;Cart-" + 0; 
  });

  
  
});


// Update price of add_button when radio selection of size change
// Input can be retrieved through name and value not id
function handleSize(radio){
  var size = radio.value;
  var itemid = radio.name;
  var item_qty = parseInt(document.querySelector(`#qty_${itemid}`).innerHTML);     
  var price = parseFloat(document.querySelector(`#price_${itemid}`).value);
  var total_price = 0.00;
  var order_price = 0.00;
    // Small(size value=3) price equal to price-3
    if (size == "3"){ 
      order_price = price - 3.00;      
    }
    // Medium(size value=1) price equal to price
    if (size == "1"){ 
      order_price = price;
    }
    // Large(size value=2) price equal to price+4
    if (size == "2"){ 
      order_price = price + 4.00;
    }
    console.log(order_price);
    total_price = order_price*item_qty;
    // Update the value of add_button with qty and total price
    document.querySelector(`#addbutton_${item_id}`).innerHTML = "Add"+ item_qty +"to Order&nbsp;&nbsp$" + total_price.toFixed(2);  
}

function getCookie(cname) {
    // Create a variable with the cname to search for
    let name = cname + "=";
    // Decode the cookie string, to handle cookies with special characters
    let decodedCookie = decodeURIComponent(document.cookie);
    // Split document.cookie on semicolons into an array called ca
    let ca = decodedCookie.split(';');
    // Loop through the ca array, and get each value c = ca[i]).
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      // If the cookie is found (c.indexOf(name) == 0), return the value of the cookie (c.substring(name.length, c.length).
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    // If the cookie is not found, return ""
    return "";
  }

  function loadoptions(){
    var start = 11;
    var end = 23;
    const d = new Date();  

    // get the value of a select
    var select = document.querySelector("#date");
    var date = select.options[select.selectedIndex].value;
  
    // If today is selected, show the remaining hours of options
    if (date.substr(0,5) == "Today"){
        document.querySelector("#time").innerHTML = "";
        for (var i =start; i<=end; i++){       
            if (i > d.getHours()){
                option =document.createElement("Option");
                option_text=document.createTextNode(i+ ":00~" + (i+1) + ":00");
                option.appendChild(option_text);                  			
                document.querySelector("#time").appendChild(option);
            }
        }
    // Other date except today is selected, show all hours of options
    } 
    if (date.substr(0,5) != "Today"){
        document.querySelector("#time").innerHTML = "";
        for (var i =start; i<=end; i++){
            option =document.createElement("Option");
            option_text=document.createTextNode(i+ ":00~" + (i+1) + ":00");
            option.appendChild(option_text);                  			
            document.querySelector("#time").appendChild(option);
         }
    }
    console.log(d.getHours());
    console.log(date);
    console.log(document.querySelector("#time").value)
    console.log(Date(date));
    console.log(d);
    console.log(date.substr(0,5))
  }
