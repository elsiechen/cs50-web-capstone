Demo video on youtube: [TaiwanCafe](https://youtu.be/l_4ng7zpHPM)

# Distinctiveness and Complexity
## Distinctiveness
This project serves as delivery website of a restaurant. Its mainly serveice is to add items from menu to cart, submit the order to the restaurant, and check the ordering history. 

## Complexity
In order.html, the popup page is at the same page of menu(order.html), and changes of item price and quantity are updated by using JavaScript without reloading the page. All order items and quantities will be stored and updated using session and local storage. 

In cart.html, user can schedule the order by choosing date from the following days and time from corresponding opening hours using JavaScript. Order items in cart are retrieved from session and quantity can be updated or removed through JavaScript. Upon change of items or quantity, amount to pay is updated without reloading the page.

# What’s contained in each file
## index.html
In this file, information about the restaurant like opening hours, address, direction link are included.

## order.html
This is the menu of the restaurant, in which items are ordered by categories. When the plus button on top right of each item is clicked, a popup form will show up on the top of this template and all buttons in menu page will be disabled temporarily. User can choose the size of the item and add or decrease quantity and then order the item to cart. The order button will update the total quantity and amount of this order item using JavaScript without reloading the page. Once order button or close button(X on left top of popup) is pressed, the popup page will be closed and user returns to the menu(this template), and all buttons in menu page will be abled again. The cart button will add this order quantity to cart. Each order item id will be stored in session. 

## cart.html
When pressing the cart button on the navbar, user will be directed to the cart. The cart button reveal the total quantity of items user has ordered, and the cart quantity was retrieved from localstorage. 

At the cart page, user is required to input the delivery address, and click on the delivery time. If deliver now button is clicked, estimate time will show "Deliver Now", else if schedule by selecting date between following seven days and selecting time between the corresponding opening hours, estimate time will show the selected result. 

Order items will be listed, and there's dropdown button in front of each item to remove or change quantity using JavaScript. User can add items by click on the "+ Add Items" button, and will be directed to menu page. User can request utensils by clicking on the checkbox, and leave note for the store for any other requests.

The form on the right will reflect the total amount of order items, delivery fee and tax will be calculated automatically based on subtotal, and finally got the total amount to be paid. Once "Place Order" button is clicked, user will be redirected to the success of order page. The item quantity in localstorage will be set to zero, the item ids will be deleted in session, and the cart button will show zero(no items in cart).

## success.html
This page shows the user has submitted order successfully,and reavls the order number and the link to details of the specific order.

## orders.html
This page shows all orders this user has made, which is in reverse chronological order. It contains all details of each order.

# How to run my application
1. install Django==1.11.11
2. run "python3 manage.py runserver" in terminal
