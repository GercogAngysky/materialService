import { addToLocalStorage } from "./storage_service.js"


export class Question {

    static async fillDataToLocalStorage(response) {
        Question.access_token = response.access_token

        return Promise.all([
            Question.addItemsToLocalStorage('price'),
            Question.addItemsToLocalStorage('maker'),
            Question.addItemsToLocalStorage('brand'),
            Question.addItemsToLocalStorage('plate'),
            Question.addItemsToLocalStorage('typedecor')
        ])
    }

    static async addItemsToLocalStorage(question) {
        await fetch(`/${question}/`, {
            method: 'GET',
            headers: {
                Authorization: "Bearer " + Question.access_token
            }
        })
        .then(response => response.json())
        .then(response => addToLocalStorage(response, question))
    }

    static async updateItem(item_id, item_data) {
        const response = await fetch(`http://127.0.0.1:8000/decor/${item_id}`, {
            method: 'PUT',
            body: item_data,
            headers: {
                'Content-Type': 'application/json',
                Authorization: "Bearer " + Question.access_token
            }
        })
        if (!response.ok) {
            const message = await response.json()
            throw new Error(message.detail)
        }
        return response.json()
    }
}
