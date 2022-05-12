
export class Footer {

    static createHtml() {
        const body = document.querySelector('body')
        const footer = document.createElement('div')
        footer.classList.add('footer')
        footer.innerHTML = `
        <footer>
            <p>©Авторские права принадлежат мне, 2022. Все права защищены.</p>
        </footer>
        `
        body.appendChild(footer)
    }
}