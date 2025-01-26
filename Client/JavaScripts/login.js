document.getElementById("login_form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const form_data = new FormData(event.target);
    const data = Object.fromEntries(form_data.entries());
    let lb_logged_in = false;
    let ls_response;

    try {
        console.log(data)
        const response = await fetch(main_api + users_api_point + "login_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        ls_response = await response.json();

        if (response.ok) {
            // alert("code of response.ok");
            if (ls_response.Success) {

                lb_logged_in = true;
            }
            else {
                alert("Invalid username or password!!!");
                return;
            }
        } else {
            alert("Failed to login!!");
        }

    } catch (error) {
        console.error("Error: " + error);
        alert("An error occurred while logging in for th user.");
    }

    if (lb_logged_in) {
        sessionStorage.setItem("logged_in_user_tran_id", ls_response.result.login_user);
        of_redirectPage("index.html");
    }
})
