fetch('http://127.0.0.1:8000/api/profile/').then(response => response.json()).then(data => initProfile(data))

function initProfile(data) {
    document.querySelector('#invite-code').textContent = data.invite_code
    if (data.code_invited === null) {
        document.querySelector('#get-invited').classList.remove('invisible')
    }
}