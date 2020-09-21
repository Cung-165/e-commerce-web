var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID:', productID, 'Action:', action)

        console.log('User:', user)
        if (user == 'AnonymousUser') {
            console.log('User is not admin')
        } else {
            updateUserOrder(productID, action)
        }
    })
}

function updateUserOrder(productID, action) {
    console.log('User is auth, sending data')
    var url = '/update_item/'
    fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Context-Type': 'application/json',

            },
            body: JSON.stringify({ 'productID': productID, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data', data)
            location.reload()
        })
}