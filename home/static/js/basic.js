function showPassword() {
    var passwordInput = document.getElementById("password");
    if (passwordInput.type == "text") {
        passwordInput.type = "password";
    } else if (passwordInput.type == "password") {
        passwordInput.type = "text";
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendByEnter(element, action, event="keyup", condition=function(event) {return event.keyCode == 13;}) {
    element.addEventListener(
        event,
        function(event) {
            if (condition(event)) {
                event.preventDefault();
                action();
            }
        }
    )
}