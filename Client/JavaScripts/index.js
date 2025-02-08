function of_logout() {
    const login_nav = document.getElementById("login-nav-item");

    login_nav.innerHTML = '<a class="nav-link">Logout</a>'

    login_nav.addEventListener("click", () => {

        let newNavItem = document.getElementById('add_new_blog_item')

        newNavItem.remove();
        sessionStorage.setItem("logged_in_user_tran_id", 0);

        newNavItem = document.getElementById('login-nav-item')

        newNavItem.innerHTML = '<a class="nav-link">Login</a>'
        newNavItem.id = 'login-nav-item'

        of_load_blogs_data();
    });
}

function of_index_file_load() {
    const logged_in_user_tran_id = sessionStorage.getItem("logged_in_user_tran_id");

    if (logged_in_user_tran_id > 0) {
        const lbl_navbar = document.getElementById("index_navbar");

        const newNavItem = document.createElement("li");
        newNavItem.innerHTML = '<a class="nav-link" href="#" onclick="of_open_add_blog()">Add New Blog</a>';

        newNavItem.classList.add("additional-nav-item");
        newNavItem.id = "add_new_blog_item"
        lbl_navbar.appendChild(newNavItem);
        of_logout();
    }
    of_load_blogs_data();
}

async function of_login(event, modal, errorMessage) {
    const form_data = new FormData(event.target);
    const data = Object.fromEntries(form_data.entries());
    let lb_logged_in = false;
    let ls_response;

    try {
        const response = await fetch(main_api + users_api_point + "login_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        ls_response = await response.json();

        if (response.status === 401) {
            return -1;
        }
        else if (response.status === 200) {
            if (ls_response.Success) {

                lb_logged_in = true;
            }
        }

    } catch (error) {
        console.error("Error: " + error);
        return -1;
    }

    if (lb_logged_in) {
        sessionStorage.setItem("logged_in_user_tran_id", ls_response.result.login_user);

        modal.style.display = "none";
        of_index_file_load();
        return 1
    }
}

function of_login_modal_configure() {
    // Get references to modal and buttons
    const modal = document.getElementById("loginModal");
    const loginButton = document.getElementById("login-nav-item");
    const closeModal = document.getElementById("closeModal");
    const loginForm = document.getElementById("loginForm");
    const errorMessage = document.getElementById("errorMessage");
    const invalid_error_msg = document.getElementById("invalidErrorMsg");
    const f_user_id = document.getElementById("user_id")
    const f_password = document.getElementById("password")
    let log_in_user = -1;

    // Show modal when "Login" button is clicked
    loginButton.addEventListener("click", () => {
        log_in_user = sessionStorage.getItem("logged_in_user_tran_id");
        if (log_in_user == 0 || log_in_user === null) {

            // show login block
            modal.style.display = "block";
            f_user_id.focus();
            return
        }
    });

    // Close modal when "X" button is clicked
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
        errorMessage.style.display = "none"; // Hide error message
        invalid_error_msg.style.display = "none"; // Hide error message
        loginForm.reset();
    });

    // Validate form input and close modal only if valid
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent default form submission

        const user_id = f_user_id.value.trim();
        const password = f_password.value.trim();

        // Check if both fields are filled
        if (user_id === "" || password === "") {
            errorMessage.style.display = "block"; // Show error message
        }

        else {
            let login_res = await of_login(event, modal, errorMessage);

            if (login_res < 0) {
                invalid_error_msg.style.display = "block"; // Show error message
            }
            else if (login_res > 0) {
                errorMessage.style.display = "none"; // Hide error message
                invalid_error_msg.style.display = "none"; // Hide error message
                alert(`Welcome, ${user_id}!`); // Simulate successful response
                modal.style.display = "none"; // Close the modal
            }
        }

        //resets the data after login attempt
        loginForm.reset();
        f_user_id.focus();
    });

    // Prevent modal from closing when clicking outside the modal content
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            errorMessage.style.display = "block";
            errorMessage.textContent = "Please complete the form before closing.";
        }
    });
}

function of_handleEdit(event) {
    const blog_id = event.target.getAttribute("data_tran_id");
    sessionStorage.setItem("blog_edit_tran_id", blog_id);
    // alert("blog to be edied" + String(blog_id));
    of_redirectPage("edit_blog.html");
}

async function of_handleDelete(event) {
    const blog_id = event.target.getAttribute("data_tran_id");
    const blog_title = event.target.getAttribute("data_blog_title");

    if (confirm(`Are you sure you want to delete blog : ${blog_title} ?`)) {
        try {
            const response = await fetch(main_api + blogs_api_point + `Delete Blog?blog_id=${blog_id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            if (!response.ok) {
                console.error("Failed to delete the blog : " + response.json());
                alert("Failed to delete the data!!");
            }

        } catch (error) {
            console.error("error while deleting the entry : " + error);
            alert("Failed to delete the data!!");
        }
        of_load_blogs_data();
    }
}

async function of_load_blogs_data() {
    let log_in_user = sessionStorage.getItem("logged_in_user_tran_id");
    try {
        let response = await fetch(main_api + blogs_api_point + "All Blogs");
        const data = await response.json()

        if (data.Success) {
            let response_data = data.result
            const blog_div_body = document.getElementById("blog_container");
            blog_div_body.innerHTML = "";

            response_data.forEach((row, index) => {
                var add_div = document.createElement("div");
                add_div.id = `blog_div_${row.blog_id}`;
                add_div.className = "blog-card";

                var add_h2 = document.createElement("h2");
                add_h2.className = "blog-title";
                add_h2.textContent = `${row.blog_title}`;
                add_div.appendChild(add_h2);

                add_div.innerHTML = add_div.innerHTML + `<p class="blog-description" >${row.blog_description}</p><p><b>By :</b> <i>${row.created_by_username}</i></p>`;
                if (log_in_user == row.created_by_user_id) {
                    add_div.innerHTML = add_div.innerHTML +
                        `<a href="#" data_tran_id = "${row.blog_id}" class="btn btn-primary edit-btn">Edit</a>` +
                        `  <a href="#" data_tran_id = "${row.blog_id}" data_blog_title = "${row.blog_title}" class="btn btn-danger delete-btn">Remove</a>`;
                }
                blog_div_body.appendChild(add_div);
            });

            document.querySelectorAll(".edit-btn").forEach(button => {
                button.addEventListener("click", of_handleEdit);
            });

            document.querySelectorAll(".delete-btn").forEach(button => {
                button.addEventListener("click", of_handleDelete);
            });
        } else {
            console.error("API returned with failure response" + data);
            alert("Failed to fetch data from API");
        }

    } catch (error) {
        console.error("Error fetching API data", error);
        alert("Unable to fetch data from the Server");
    }
}

function of_open_add_blog() {
    of_redirectPage("add_blog.html");
}

// function to be call at time of index.html loaded
of_index_file_load();

//function to set the listeners for login modal and login button
of_login_modal_configure();