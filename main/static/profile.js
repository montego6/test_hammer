fetch('http://127.0.0.1:8000/api/profile/').then(response => response.json()).then(data => initProfile(data))

const csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value

function initProfile(data) {
    console.log(data)
    document.querySelector('#invite-code').textContent = data.invite_code
    if (data.code_invited === null) {
        document.querySelector('#get-invited').classList.remove('invisible')
    }
}

document.querySelector('#button-get-invited').addEventListener('click', event => {
    const invite_code = document.querySelector('input[name=code-invited]').value
    data = {
        invite_code: invite_code
    }
    fetch('http://127.0.0.1:8000/api/get-invited/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrf_token,
          },
        body: JSON.stringify(data)
    }).then(response => response.json())
})