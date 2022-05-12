import { Main } from "./cmp_main.js"
import { StorageService } from "./storage_service.js"


export class Pagination {

    static createHtml() {

        const pagination_pages = document.createElement('div')
        pagination_pages.classList.add('pagination-pages')
        pagination_pages.appendChild(getListNumPages())
        
        if (document.getElementById('pagination')) {
            const pagination = document.getElementById('pagination')
            pagination.innerHTML = ''
            pagination.appendChild(pagination_pages)
        }
        else {
            const pagination = document.createElement('div')
            pagination.id = 'pagination'
            pagination.appendChild(pagination_pages)
            document.querySelector('body').appendChild(pagination)
        }
    }
}

function getPageNum(num) {
    const pageNum = document.createElement('li')
    pageNum.classList.add('pagination-pages')
    pageNum.classList.add('page')
    pageNum.innerHTML = num
    pageNum.addEventListener('click', () => {
        document.getElementsByClassName('activate')[0].classList.remove('activate')
        pageNum.classList.add('activate')
        Main.createHtml()
    })
    return pageNum
}

function getListNumPages() {
    const countOfPages = Math.ceil(StorageService.filterData().length / countOfItemsOnPage)
    const listNums = document.createElement('ul')
    // create first number
    const firstNum = getPageNum(1)
    firstNum.classList.add('activate')
    listNums.appendChild(firstNum)
    // create other numbers
    for (let num = 1; num < countOfPages; num++) {
        listNums.appendChild(
            getPageNum(num+1)
        )
    }
    return listNums
}

    export const countOfItemsOnPage = 20
