const csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value

document.querySelector('#login-code-button').addEventListener('click', event => {
    const phone_number = document.querySelector('input[name=phone_number]').value
    const data = {
        phone_number: phone_number
    }
    fetch('http://127.0.0.1:8000/api/login/code/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrf_token,
          },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(data => {
        console.log(data)
        if (data.status === 'success') {
            document.querySelector('#login-first-step').classList.add('invisible')
            document.querySelector('#login-second-step').classList.remove('invisible')
            document.querySelector('#login-second-step p span').textContent = data.code
        }
    })
})

document.querySelector('#login-button').addEventListener('click', event => {
    const phone_number = document.querySelector('input[name=phone_number]').value
    const code = document.querySelector('input[name=code]').value
    const data = {
        phone_number: phone_number,
        code: code,
    }
    fetch('http://127.0.0.1:8000/api/login/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrf_token,
          },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = 'http://127.0.0.1:8000/profile/';
        } 
        return response.json() 
    }).then(data => console.log(data))
})