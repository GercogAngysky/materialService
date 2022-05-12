
export const queryData = function(element) {
    const btn = document.querySelector("button");
    
    btn.addEventListener("click", async function(event) {
        event.preventDefault();
        let response_token = await fetch('/auth/sign-in', {
            method: 'POST',
            body: new FormData(document.querySelector('form'))
        });
        if (response_token.ok){
            let token = await response_token.json();
            let response = await fetch('/price', {
                method: 'GET',
                headers: {
                    Authorization: "Bearer " + token.access_token
                }
            });
            response.json()
            .then(data => {
                // element.innerHTML = ''
                for(let item of data.slice(0, 100)) {
                    addMaterial(item)
                }
            });
        } else {
            window.location.href = '/index'
        }
    });
}

// document.addEventListener("DOMContentLoaded", function(){
// })
