const main_api = "http://127.0.0.1:8000/"
const users_api_point = "user/"
const blogs_api_point = "blogs/"

function of_redirectPage(as_page) {
    window.location.href = as_page
}

function of_return_to_index() {
    of_redirectPage("index.html");
}