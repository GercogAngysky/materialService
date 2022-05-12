import { countOfItemsOnPage } from "./cmp_pagination.js"
import { StorageService} from "./storage_service.js"
import { Modal } from "./cmp_modal.js"
import { Question } from './questions.js'

export class Main {

    static createHtml() {
        // claculate slice range of Storage data
        const beginRange = (+document.getElementsByClassName('activate')[0].textContent-1)*countOfItemsOnPage
        const endRange = beginRange + countOfItemsOnPage
        const data =  StorageService.filterData().slice(beginRange, endRange)

        // create items with data and fill in main block
        const html = (data.length
            ? data.map(toCard).join('')
            : `<div style="text-align: center">NOT CONTENT</div>`
        )
        if (document.getElementById('main')) {
            document.getElementById('main').innerHTML = html
        }
        else {
            const main = document.createElement('div')
            main.id = 'main'
            main.innerHTML = html
            document.querySelector('body').appendChild(main)
        }

        // add handler overlay for items
        const links_items = document.querySelectorAll('.name-item')
        const modalOverlay = document.querySelector('.modal-overlay')
        
        links_items.forEach((element) => {
            element.addEventListener('click', (event) => {
                let item_id = event.currentTarget.getAttribute('data_target')
                
                const form = Modal.createForm(element.textContent)
                
                form.addEventListener('submit', (event) => {
                    event.preventDefault()
                    const input = form.querySelector('input')
                    Question.updateItem(item_id, JSON.stringify({"name": input.value}))
                    .then(response => element.textContent = response.name)
                    .then(() => {
                        modalOverlay.classList.remove('modal-overlay--visible')
                        form.classList.remove('modal--visible')
                    })




                    .then( Question.addItemsToLocalStorage('price') ) //reload data from server to localStorage
 
 
 
 
                    .catch(error => form.innerHTML = error)
                })

                modalOverlay.replaceChildren(form)

                modalOverlay.classList.add('modal-overlay--visible')
                form.classList.add('modal--visible')

                modalOverlay.addEventListener('click', (event) => {
                    if (event.target == modalOverlay) {
                        modalOverlay.classList.remove('modal-overlay--visible')
                        form.classList.remove('modal--visible')
                    }
                })
            })
        })
        // const main = (
        //     document.getElementById('main') || document.createElement('div')
        // )
        // main.id = 'main'
    }
}


function toCard(item) {
    return `
        <div class="wraper-item">
            <div class="image-item">
                <img src="static/img/ldsp.jpg" alt=""/>
            </div>
            <table class="info-item">
                <tbody>
                    <tr>
                        <td class="name-item" data_target=${item.material.decor.id}>${item.material.decor.name}</td>
                        <td class="price">${item.value} ${item.currency}</td>
                    </tr>
            </tbody>
            </table>
        </div>
        `
}
