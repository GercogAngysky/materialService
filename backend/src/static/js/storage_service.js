
export class StorageService {

    static filterData() {

        return (getFromLocalStorage('price')
            .filter(checkBrand)
            .filter(checkMaker)
            .filter(checkTypeDecor)
            .filter(checkThickness)
            .sort(compareItems)
        )
    }
}


function compareItems (a, b) {
    if (a.value > b.value) {
      return 1
    }
    if (a.value < b.value) {
      return -1
    }
    return 0
  }


function addToLocalStorage(response, question) {
    const all = getFromLocalStorage(question)
    all.push(response)
    localStorage.setItem(question, JSON.stringify(response))
}

function getFromLocalStorage(question) {
    return JSON.parse(localStorage.getItem(question) || '[]')
}

// function updateItemToLocalStorage(item_id, item_data) {
//     const data = getFromLocalStorage('price')
//     data.forEach(element => {
//         if element.material.decor.
//     });
// }



// filters:

function checkBrand(item) {
    const value = document.getElementById('brand').value
    return value != 'all'
        ? item.material.brand.name == value
        : true
}

function checkMaker(item) {
    const value = document.getElementById('maker').value
    return value != 'all'
        ? item.maker.name == value
        : true
}

function checkTypeDecor(item) {
    const value = document.getElementById('typedecor').value
    return value != 'all'
        ? item.material.decor.typedecor.name == value
        : true
}

function checkThickness(item) {
    const value = document.getElementById('thickness').value
    return value != 'all'
        ? item.material.plate.thickness == value
        : true
}

export { getFromLocalStorage, addToLocalStorage }
