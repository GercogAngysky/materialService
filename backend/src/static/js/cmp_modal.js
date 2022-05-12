

export class Modal {

    static createHtml() {
        const modal = document.createElement('div')
        modal.classList.add('modal-overlay')
        // modal.innerHTML = `
        //     <form class="modal modal-form" name="name" method="PUT" action="/decor/">
        //         <input type="text" id="itemname"/>
        //         <button id="submit_edit" type="submit">
        //             edit
        //         </button>
        //     </form>
        // `
        document.querySelector('body').appendChild(modal)
    }

    static createForm(text) {
        const form = document.createElement('form')
        const input = document.createElement('input')
        const button = document.createElement('button')

        form.classList.add('modal')
        form.classList.add('modal-form')
        form.setAttribute('name', 'name')
        form.setAttribute('method', 'PUT')
        // form.setAttribute('action', '/decor/')

        input.setAttribute('type', 'text')
        input.setAttribute('id', 'itemname')
        input.value = text

        button.setAttribute('id', 'submit_edit')
        button.innerHTML = 'edit'

        form.appendChild(input)
        form.appendChild(button)

        return form
    }
}
