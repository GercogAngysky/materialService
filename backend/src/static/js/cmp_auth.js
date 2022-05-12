
export class Auth {

    static createFormHtml() {
        document.querySelector('body').innerHTML = `
        <div id="auth" class="auth">
            <form id="auth-form" class="auth-form"  method="POST" action="/auth/sign-in">
                <input type="text" id="username" name="username" placeholder="username"/>
                <input type="password" id="password" name="password" placeholder="password"/>
                <button id="submit" type="submit">
                    <img src="static/img/shkafstudy.ico" alt="logo ШкафСтудия"/>
                </button>
            </form>
        </div>
        `

        Auth.auth = document.getElementById('auth')
        Auth.form = Auth.auth.querySelector('#auth-form')
        Auth.username = Auth.auth.querySelector('#username')
        Auth.password = Auth.auth.querySelector('#password')
        Auth.submitBtn = Auth.auth.querySelector('#submit')

        Auth.setStyle('start')

        Auth.form.addEventListener('input', () => {
            if (Auth.username.value.length && Auth.password.value.length) {
                Auth.setStyle('enter')
            }
            else {
                Auth.setStyle('start')
            }
        })
    }

    static setStyle(mode) {
        const color = {
            start: 'gainsboro',
            enter: 'gainsboro',
            error: 'magenta'
        }
        const disabled = {
            start: true,
            enter: false,
            error: true
        }
        const opacity = {
            start: 0.5,
            enter: 1,
            error: 0.5
        }
        Auth.username.style.borderColor = color[mode]
        Auth.password.style.borderColor = color[mode]
        Auth.submitBtn.disabled = disabled[mode]
        Auth.submitBtn.style.opacity = opacity[mode]
    }

    static async getAllowed() {
        const response = await fetch('/auth/sign-in', {
            method: 'POST',
            body: new FormData(Auth.form),
        })
        if (!response.ok) {
            Auth.setStyle('error')
            const message = await response.json()
            throw new Error(message.detail)
        }
        return response.json()
    }
}
