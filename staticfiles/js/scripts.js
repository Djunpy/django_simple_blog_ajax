const header = document.querySelector('header')
const searchForm = document.querySelector('.header__search-form')
const loginFormDiv = document.querySelector('.form__login')
const mainPost = document.querySelector('.main__post')
const loadBtn = document.querySelector('#load-btn')
const headerNavbarDropdownContent = document.querySelector('.header__navbar-dropdown-content')
const searchInput = document.querySelector('#id_search')
const resultSearch = document.querySelector('.result-search')
const categoryLink = document.querySelectorAll('#category-link')
const formlogin = document.querySelector('#form__login')
const url = window.location.href
const userAlert = document.querySelector('.user_alert')
const userAlertText = document.querySelector('.user_alert-text')
const registerForm = document.querySelector('#form-register')


function handlerHeader(e){

    if (e.target.id === 'search-btn'){
        searchForm.classList.toggle('active')
        loginFormDiv.classList.remove('active')
    }
    if (e.target.id === 'login-btn'){
        loginFormDiv.classList.toggle('active')
        searchForm.classList.remove('active')
    }
}

function loginSendData(e){
    e.preventDefault()
    data = new FormData(e.target)
    response = makeDataRequest('/accounts/login/', data)
        .then(res => res.json())
        .then(res => res)
        .catch(err => err)

    if (response.ok){
        username = document.querySelector('#id_login').value
        userAlertText.innerText = `Добро пожаловать!, ${username}`
        userAlert.classList.add('successfully')
        setTimeout(() =>{
            loginFormDiv.classList.toggle('active')
        }, 2000)
    }
}

function registerSendData(e){
    e.preventDefault()
    data = new FormData(e.target)
    response = makeDataRequest('/accounts/signup/', data)
        .then(res => res.json())
        .then(res => res)
        .catch(err => err)
    console.log(response)
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


async function makeJsonRequest(url, method, body) {
     headers = {
         "X-Requested-With": "XMLHttpRequest",
          'Content-Type': 'application/json'
    }
    if (method === 'POST'){
        headers['X-CSRFToken'] = csrftoken
    }

    let response = await fetch(url, {
        method: method,
        headers: headers,
        body: body,
    })
    if (!response.ok){
        throw Error(response.statusText)
    }else{
        return await response
    }


}

async function makeDataRequest(url, body){
      headers = {
         "X-Requested-With": "XMLHttpRequest",
          'X-CSRFToken': csrftoken
      }

    const response = await fetch(url, {
        method: 'POST',
        headers: headers,
        body: body
    })
     if (!response.ok){
        throw Error(response.statusText)
    }else{
         return await response
     }
}


async function sendSearchData(data){
    await makeJsonRequest('/search/', 'POST', JSON.stringify({'q': data}))
        .then(response => response.json())
        .then(async response => {
            const search_data = await response.search_data
            if (search_data.length){
                resultSearch.innerHTML = ''
                search_data.forEach(el =>{
                    resultSearch.innerHTML +=`
                        <div class="result-search__box">
                            <img src="${el.image}" alt="" class="result-search__img">
                                <div class="result-search__desc">
                                    <h3><a href="/post/${el.id}">${el.title}</a></h3>
                                </div>
                        </div>`
                })
            }else {

                resultSearch.classList.remove('active')
            }

        })
        .catch(err => err)
}

let page = 1

async function getAllPosts(){
    response = await makeJsonRequest(`/?page=${page}`, 'GET')
        .then(res => res.json())
        .then(async res => {
            return await res
        })
        .catch(err => err)
    mainPost.innerHTML = ''
    renderPosts(response)
}

getAllPosts(renderPosts)

async function getPostsByCategory(categoryId){
    response = await makeJsonRequest(`/category/${categoryId}/?page=${page}`, 'GET')
        .then(res => res.json())
        .then(async res => await res)
        .catch(err => err)
    console.log(response)
    console.log(url)
    renderPosts(response)
    mainPost.innerHTML = ''
}

async function renderPosts(response){

    const data = response.object_list

    try {
        setTimeout(()=> {
            data.forEach(el => {
                 mainPost.innerHTML +=
                    `
                    <div class="main__post-box">
                        <img src="${el.image}" alt="" class="main__post-img"> 
                        <h2 class="main__post-category">${el.category}</h2>
                        <a href="/post/${el.id}" class="main__post-title">${el.title}</a>
                        <span class="main__post-date">${el.published}</span>
                        <p class="main__post-description">${el.description}</p>
                        <div class="main__post-author">
                            <div class="main__post-author-group">
                                <img src="${el.author_avatar}" alt="" class="main__author-img">
                                    <span class="post__author-name">${el.author_name}</span>
                            </div>
                            <div class="main__post-author-eye"><span>${el.views}</span><span><i
                                class='bx bxs-binoculars'></i></span>
                            </div>
                        </div>
                    </div>
                    `
            }, 200)
        mainPost.append(loadBtn)
        })
    }catch (err){
        return err
    }

}



header.addEventListener('click', handlerHeader)

loginFormDiv.addEventListener('click', (e)=> {
    if (e.target.id === 'close-form__login'){
        console.log(e.target)
        loginFormDiv.classList.toggle('active')
    }
    if (e.target.id === 'for-register'){
        console.log(e.target)
        loginFormDiv.classList.toggle('active')
        registerForm.classList.add('active')
    }
})

formlogin.addEventListener('submit', loginSendData)

registerForm.addEventListener('submit', registerSendData)

mainPost.addEventListener('click', (e)=>{
    e.preventDefault()
    if (e.target.id === 'load-btn'){
        console.log(url)
        ++page
        getAllPosts(renderPosts)
    }
})

window.addEventListener('scroll', () => {
    header.classList.toggle('shadow', window.scrollY > 0)
    headerNavbarDropdownContent.classList.toggle('shadow', window.scrollY > 0)

})

searchInput.addEventListener('keyup', (e)=> {
    if (e.target.value.length){
        resultSearch.classList.add('active')
    }else{
        resultSearch.classList.remove('active')
    }

    sendSearchData(e.target.value)
})


categoryLink.forEach(link => {
    link.addEventListener('click', evt => {
        evt.preventDefault()
        categoryId = evt.target.dataset.categoryId
        getPostsByCategory(categoryId, renderPosts)
    })
})




//
// let visible = 4
//
// async function getPosts(renderPosts){
//     response = await makeRequest(`/posts/${visible}/`,'GET')
//         .then(response => response.json())
//         .then(async response => {
//             return await response
//         })
//         .catch(err => err)
//     renderPosts(response)
// }
//
// getPosts(renderPosts)
//
//
// async function getPostsByCategory(categoryId){
//     response = await makeRequest(`/categories/${categoryId}/`, 'GET')
//         .then(res => res.json())
//         .then(async res => await res)
//         .catch(err => err)
//     console.log(response)
//     renderPosts(response)
//     mainPost.innerHTML = ''
// }
//
//
// async function renderPosts(response){
//     const data = response.object_list
//     console.log(data)
//     try {
//         setTimeout(()=> {
//             data.forEach(el => {
//                  mainPost.innerHTML +=
//                     `
//                     <div class="main__post-box">
//                         <img src="${el.image}" alt="" class="main__post-img">
//                         <h2 class="main__post-category">${el.category}</h2>
//                         <a href="/post/${el.id}/" class="main__post-title">${el.title}</a>
//                         <span class="main__post-date">${el.published}</span>
//                         <p class="main__post-description">${el.description}</p>
//                         <div class="main__post-author">
//                             <div class="main__post-author-group">
//                                 <img src="${el.author_avatar}" alt="" class="main__author-img">
//                                     <span class="post__author-name">${el.author_name}</span>
//                             </div>
//                             <div class="main__post-author-eye"><span>${el.views}</span><span><i
//                                 class='bx bxs-binoculars'></i></span>
//                             </div>
//                         </div>
//                     </div>
//                     `
//             }, 200)
//         })
//     }catch (err){
//         return err
//     }
//
// }

