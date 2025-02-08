function of_form_submit_code() {
    document.getElementById("add_blog_form").addEventListener("submit", async function (event) {
        event.preventDefault();
        const login_user = sessionStorage.getItem("logged_in_user_tran_id");

        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(main_api + blogs_api_point + `Create Blog?user_id=${login_user}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!(response.ok)) {
                alert("Failed to publish data!!!");
            }
            else {
                alert("Blog published successfully!!");
            }
        } catch (error) {
            console.error("Error: " + error);
            alert("An error occurred while publishing data1!!");
        }
        of_return_to_index();
    });
}

of_form_submit_code();

document.getElementById("blogs_title").focus();