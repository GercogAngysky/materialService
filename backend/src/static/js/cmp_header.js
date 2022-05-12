import { Main } from "./cmp_main.js"
import { Pagination } from "./cmp_pagination.js";
import { getFromLocalStorage } from "./storage_service.js"

export class Header {

    static createHtml() {
        document.querySelector('body').innerHTML = `
        <header class="header">
            <nav class="menu">
                <div class="header-logo">
                    <a href="" id="hs-link">
                        <img src="static/img/shkafstudy.ico"
                            class="hs-image"
                            alt=""
                            sizes="(max-width: 1040px) 100vw, 1040px"
                        >
                    </a>
                </div>
                <div class="header-menu">
                    <form id="query">
                        <select id="brand">
                            <option>all</option>
                            ${createOptions('brand')}
                        </select>
                        <select id="maker">
                            <option>all</option>
                            ${createOptions('maker')}
                        </select>
                        <select id="typedecor">
                            <option>all</option>
                            ${createOptions('typedecor')}
                        </select>
                        <select id="thickness">
                            <option>all</option>
                            ${createOptions('plate')}
                        </select>
                    </form>
                </div>
            </nav>
        </header>
        `
        document.getElementById('brand').addEventListener('change', (e) => {Pagination.createHtml(); Main.createHtml()})
        document.getElementById('maker').addEventListener('change', (e) => {Pagination.createHtml(); Main.createHtml()})
        document.getElementById('typedecor').addEventListener('change', (e) => {Pagination.createHtml(); Main.createHtml()})
        document.getElementById('thickness').addEventListener('change', (e) => {Pagination.createHtml(); Main.createHtml()})
    }
}


function createOptions(option) {
    const data = getFromLocalStorage(option)
    const html = data.length
        ? data.map(toCard).join('')
        : 'not content'
    return html
}

function toCard(item) {
    if (item.name) {
        return `
            <option>${item.name}</option>
        `
    }
    return `<option>${item.thickness}</option>`
}
