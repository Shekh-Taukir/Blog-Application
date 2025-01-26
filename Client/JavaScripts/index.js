function of_logout() {
    const login_nav = document.getElementById("login-nav-item");

    login_nav.innerHTML = '<a class="nav-link">Logout</a>'

    login_nav.addEventListener("click", () => {
        // alert("Logout code is ready to drive in")
        let newNavItem = document.getElementById('add_new_blog_item')
        // alert(newNavItem.innerHTML)
        newNavItem.remove();
        sessionStorage.setItem("logged_in_user_tran_id", 0);

        newNavItem = document.getElementById('login-nav-item')

        newNavItem.innerHTML = '<a class="nav-link">Login</a>'
        newNavItem.id = 'login-nav-item'
        // of_redirectPage("index.html");
    });
}

function of_login() {
    const logged_in_user_tran_id = sessionStorage.getItem("logged_in_user_tran_id");

    if (logged_in_user_tran_id > 0) {
        const lbl_navbar = document.getElementById("index_navbar");

        const newNavItem = document.createElement("li");
        newNavItem.innerHTML = '<a class="nav-link" href="#">Add New Blog</a>';

        newNavItem.classList.add("additional-nav-item");
        newNavItem.id = "add_new_blog_item"
        lbl_navbar.appendChild(newNavItem);
        of_logout();
    }
}
of_login()