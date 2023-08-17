document.querySelector('#login-button').addEventListener('click', event => {
    const phone_number = document.querySelector('input[name=phone_number]').value
    const data = {
        phone_number: phone_number
    }
    fetch('http://127.0.0.1:8000/api/login/get-code/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
          },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(data => console.log(data))
})