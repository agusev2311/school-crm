// src/api/files_api.js
import api_client from './client.js';  // предполагается, что client.js уже есть

export async function importObjects(file) {
    // Готовим FormData для передачи файла
    const formData = new FormData();
    formData.append('file', file);

    // Делаем POST-запрос на /files
    const response = await api_client.fetch(`/import/objects`, {
        method: 'POST',
        body: formData
    }, '');

    return response.result;
}
export async function importSubmissions(file) {
    // Готовим FormData для передачи файла
    const formData = new FormData();
    formData.append('file', file);

    // Делаем POST-запрос на /files
    const response = await api_client.fetch(`/import/submissions`, {
        method: 'POST',
        body: formData
    }, '');

    return response.result;
}