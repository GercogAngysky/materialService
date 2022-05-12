import { Auth } from "./cmp_auth.js"
import { Header } from "./cmp_header.js"
import { Main } from "./cmp_main.js"
import { Footer } from "./cmp_futer.js"
import { Question } from "./questions.js"
import { Pagination } from "./cmp_pagination.js"
import { Modal } from "./cmp_modal.js"


window.addEventListener('load', function() {
    Auth.createFormHtml()
    Auth.form.addEventListener('submit', (event) => {
        event.preventDefault()
        Auth.getAllowed()
        .then( Question.fillDataToLocalStorage )
        .then( Header.createHtml )
        .then( Pagination.createHtml )
        .then( Modal.createHtml )
        .then( Main.createHtml )
        .then( Footer.createHtml )
        .catch(error => console.log(error))
    })
})
